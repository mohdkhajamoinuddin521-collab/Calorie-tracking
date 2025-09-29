from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_calorie_goal = models.PositiveIntegerField(default=2000)  # optional per-user setting

    def __str__(self):
        return f"Profile({self.user.username})"

MEAL_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
]

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField()  # allows filtering by day
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def calories(self):
        # sum of related food item calories
        return sum(item.calories for item in self.food_items.all())

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"

class FoodItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    quantity = models.FloatField(default=1.0)  # allow quantities if needed (optional)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_calories(self):
        return int(self.calories * self.quantity)

    def __str__(self):
        return f"{self.name} ({self.total_calories()} kcal)"
