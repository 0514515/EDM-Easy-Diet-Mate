from django.db import models

class Nutrient(models.Model):
    food_name = models.CharField(db_column='Food_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    weight_g = models.FloatField(blank=True, null=True)
    energy_kcal = models.FloatField(db_column='Energy_kcal', blank=True, null=True)  # Field name made lowercase.
    carbs_g = models.FloatField(blank=True, null=True)
    sugar_g = models.FloatField(blank=True, null=True)
    fat_g = models.FloatField(blank=True, null=True)
    protein_g = models.FloatField(blank=True, null=True)
    nat_mg = models.FloatField(blank=True, null=True)
    col_mg = models.FloatField(blank=True, null=True)
    nutrient_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'nutrient'


class Usermeal(models.Model):
    # usermeal_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    meal_type = models.TextField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    food_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'usermeal'


class Usermealevaluation(models.Model):
    user_id = models.IntegerField(primary_key=True)
    meal_date = models.DateField(blank=True, null=True)
    sys_config = models.FloatField(blank=True, null=True)
    sum_carb = models.FloatField(blank=True, null=True)
    sum_sugar = models.FloatField(blank=True, null=True)
    sum_protein = models.FloatField(blank=True, null=True)
    sun_fat = models.FloatField(blank=True, null=True)
    meal_evaluation = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usermealevaluation'


class Usermealnutrientlink(models.Model):
    usermeal = models.ForeignKey(Usermeal, models.CASCADE) # The composite primary key (usermeal_id, nutrient_id) found, that is not supported. The first column is selected.
    nutrient = models.ForeignKey(Nutrient, models.CASCADE)

    class Meta:
        db_table = 'usermealnutrientlink'
        unique_together = (('usermeal', 'nutrient'),)
