from django.db import models

class Meal_Date(models.Model):
     
    # 데일리 식사에 대한 정보
    user_uid = models.IntegerField(default = 0, null = False)
    meal_type = models.CharField(defalut = '', null = False)
    
    meal_kcal = models.FloatField(default = 0.0, null = False)
    meal_carb = models.FloatField(default = 0.0, null = False)
    meal_pro = models.FloatField(default = 0.0, null = False)
    meal_fat = models.FloatField(default = 0.0, null = False)
    meal_nat = models.FloatField(default = 0.0, null = False)
    meal_col = models.FloatField(default = 0.0, null = False)
    
    meal_evaluation = models.CharField(defalut = '', null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateField(auto_now=True)
    link = models.TextField()
    def __str__(self):
        return f"Meal_Date {self.id})"
        

