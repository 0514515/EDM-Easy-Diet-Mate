from django.db import models

class Nutrient(models.Model):
    # 음식에 대한 영양 정보
    food_name = models.CharField(default = '', null = False, max_length = 45)
    meal_gram = models.FloatField(default = 0.0, null = False)
    
    meal_kcal = models.FloatField(default = 0.0, null = False)
    meal_carb = models.FloatField(default = 0.0, null = False)
    meal_sugars = models.FloatField(default = 0.0, null = False)
    meal_fat = models.FloatField(default = 0.0, null = False)
    meal_pro = models.FloatField(default = 0.0, null = False)
    meal_nat = models.FloatField(default = 0.0, null = False)
    meal_col = models.FloatField(default = 0.0, null = False)
    nutrient_id = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return self.food_name
    
class UserMeal(models.Model):
    # 식사를 저장한 유저 정보 추가 해야함
    usermeal_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    meal_type = models.CharField(default = '', null = False, max_length = 10)
    created_at = models.DateTimeField(auto_now_add=True)# 저장된 날짜
    link = models.TextField()# 사진 링크
    foods = models.ManyToManyField(Nutrient, through = 'UserMealNutrientLink')
    
    def __str__(self):
        return f"{', '.join([food.food_name for food in self.foods.all()])} - {self.meal_type}"

class UserMealNutrientLink(models.Model):
    usermeal_id = models.IntegerField()
    nutrient_id = models.IntegerField()
    
    # Foreign Keys
    usermeal_id = models.ForeignKey(UserMeal, on_delete=models.CASCADE)
    nutrient_id = models.ForeignKey(Nutrient, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('usermeal_id', 'nutrient_id'),)

    def __str__(self):
        return f"{self.usermeal.meal_type} - {self.nutrient.food_name}"

# class MealFood(models.Model):
#     meal_date = models.ForeignKey(User_Meal, on_delete = models.CASCADE)
#     food = models.ForeignKey(Nutrition, on_delete = models.CASCADE)
#     quantity = models.PositiveBigIntegerField(default = 1)

class UserMealEvaluation(models.Model):
    user_id = models.IntegerField(primary_key=True)
    meal_date = models.DateField()
    sys_config = models.FloatField()
    sum_carb = models.FloatField()
    sum_sugar = models.FloatField()
    sum_protein = models.FloatField()
    sun_fat = models.FloatField()
    meal_evaluation = models.TextField()

    def __str__(self):
        return f"{self.user_id} - {self.meal_date}"


    

        

