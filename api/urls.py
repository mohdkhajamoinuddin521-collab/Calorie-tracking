from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, FoodItemViewSet, RegisterView, calorie_summary
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'meals', MealViewSet, basename='meal')
router.register(r'food-items', FoodItemViewSet, basename='fooditem')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('summary/', calorie_summary, name='calorie-summary'),
]
