from django.db import models
import uuid

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

    class Meta:
        db_table = 'nutrient'


class Usermeal(models.Model):
    # id = models.AutoField(primary_key = True)
    #user_id = models.CharField(max_length=255, null=False)
    user_id = models.UUIDField(default=uuid.uuid4, max_length=32)
    meal_type = models.TextField(blank=True, null=True)
    meal_date = models.DateField(blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    food_name = models.ForeignKey(Nutrient, on_delete=models.CASCADE, to_field='food_name', related_name='usermeals')
    class Meta:
        db_table = 'usermeal'


class Usermealevaluation(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, max_length=32)
    meal_date = models.DateField(blank=True, null=True)
    sum_carb = models.FloatField(blank=True, null=True)
    sum_sugar = models.FloatField(blank=True, null=True)
    sum_protein = models.FloatField(blank=True, null=True)
    sun_fat = models.FloatField(blank=True, null=True)
    meal_evaluation = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usermealevaluation'
