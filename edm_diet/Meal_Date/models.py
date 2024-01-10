from django.db import models
from uuid import *


# 음식의 영양정보가 저장되어 있는 모델
class Nutrient(models.Model):
    food_name = models.CharField(db_column='Food_Name', max_length=45, primary_key=True)  # Field name made lowercase.
    weight_g = models.FloatField(blank=True, null=True)
    energy_kcal = models.FloatField(db_column='Energy_kcal', blank=True, null=True)  # Field name made lowercase.
    carbs_g = models.FloatField(blank=True, null=True)
    sugar_g = models.FloatField(blank=True, null=True)
    fat_g = models.FloatField(blank=True, null=True)
    protein_g = models.FloatField(blank=True, null=True)
    nat_mg = models.FloatField(blank=True, null=True)
    col_mg = models.FloatField(blank=True, null=True)

    def serialize(self):
        return {
            "food_name": self.food_name,
            "weight_g": self.weight_g,
            "energy_kcal": self.energy_kcal,
            "carbs_g": self.carbs_g,
            "sugar_g": self.sugar_g,
            "fat_g": self.fat_g,
            "protein_g": self.protein_g,
            "nat_mg": self.nat_mg,
            "col_mg": self.col_mg,
        }
        
    class Meta:
        db_table = 'nutrient'
    
# 이미지 주소를 받아와 변환하는 함수
def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid4()}.{ext}"
    return new_filename

# 사용자의 식단이 저장되어 있는 모델
class Usermeal(models.Model):
    uuid = models.UUIDField(default=uuid4, max_length=32)
    meal_type = models.TextField(blank=True, null=True)
    meal_date = models.DateField(blank=True, null=True)
    imagelink = models.ImageField(upload_to=get_image_filename, max_length=3000)
    food_name = models.ForeignKey(Nutrient, on_delete=models.CASCADE, to_field='food_name', related_name='usermeals')
    meal_serving = models.FloatField(blank=True, null=True)
        
    def serialize(self):
        return {
            "uuid": self.uuid,
            "meal_type": self.meal_type,
            "meal_date": self.meal_date,
            "imagelink": self.imagelink,
            "food_name": self.food_name,
            "meal_serving": self.meal_serving,
        }
    
    class Meta:
        db_table = 'usermeal'

# 사용자의 식단에 대한 평가와 정보가 저장되어 있는 모델
class Usermealevaluation(models.Model):
    uuid = models.UUIDField(default=uuid4, max_length=32)
    meal_date = models.DateField(blank=True, null=True)
    sum_carb = models.FloatField(blank=True, null=True)
    sum_sugar = models.FloatField(blank=True, null=True)
    sum_protein = models.FloatField(blank=True, null=True)
    sum_fat = models.FloatField(blank=True, null=True)
    sum_kcal = models.FloatField(blank=True, null=True)
    sum_nat = models.FloatField(blank=True, null=True)
    sum_col = models.FloatField(blank=True, null=True)
    meal_evaluation = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usermealevaluation'
        
class Imagesave(models.Model):
    id = models.AutoField(primary_key=True)
    imagelink = models.ImageField(upload_to=get_image_filename, max_length=3000)
    
    class Meta:
        db_table = 'Imagesave'