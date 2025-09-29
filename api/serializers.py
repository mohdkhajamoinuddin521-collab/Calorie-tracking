from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Meal, FoodItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class FoodItemSerializer(serializers.ModelSerializer):
    total_calories = serializers.SerializerMethodField()
    class Meta:
        model = FoodItem
        fields = ['id','meal','name','calories','quantity','created_at','total_calories']
        read_only_fields = ['created_at','total_calories']

    def get_total_calories(self, obj):
        return obj.total_calories()

class MealSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True, read_only=True)
    calories = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id','user','date','meal_type','created_at','food_items','calories']
        read_only_fields = ['user','created_at','calories']

    def get_calories(self, obj):
        return obj.calories()

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user','daily_calorie_goal']
