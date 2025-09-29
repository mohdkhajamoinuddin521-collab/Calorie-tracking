from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Meal, FoodItem, Profile
from .serializers import (
    UserSerializer, RegisterSerializer,
    MealSerializer, FoodItemSerializer, ProfileSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum, F

# Registration view
from rest_framework.views import APIView

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # return tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Meals ViewSet
class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# FoodItem ViewSet
class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only food items for meals owned by the user
        return FoodItem.objects.filter(meal__user=self.request.user)

    def perform_create(self, serializer):
        # ensure the meal belongs to the user
        meal = serializer.validated_data['meal']
        if meal.user != self.request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

# Profile / stats endpoint
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def calorie_summary(request):
    """
    Returns calories_eaten, calories_burned (optional), calories_remaining for the current day.
    calories_burned: for MVP, we allow storing in profile or return 0; could integrate with activity trackers.
    """
    user = request.user
    date = request.query_params.get('date')  # optional YYYY-MM-DD; if not provided use today
    from datetime import date as dt_date
    if not date:
        date = dt_date.today()

    # total calories eaten for date
    eaten = FoodItem.objects.filter(meal__user=user, meal__date=date).aggregate(
        total=Sum(F('calories') * F('quantity'))
    )['total'] or 0

    # burned: simple approach - stored in profile or 0 (you can extend)
    profile = Profile.objects.get(user=user)
    calories_burned = getattr(profile, 'calories_burned_today', 0) if hasattr(profile, 'calories_burned_today') else 0

    remaining = profile.daily_calorie_goal - eaten + calories_burned

    return Response({
        'date': str(date),
        'calories_eaten': int(eaten),
        'calories_burned': int(calories_burned),
        'calories_remaining': int(remaining),
        'daily_goal': profile.daily_calorie_goal
    })
