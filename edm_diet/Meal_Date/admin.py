from django.contrib import admin
from .models import *


class UsermealAdmin(admin.ModelAdmin):
    model = Usermeal
    list_display = ('uuid', 'meal_date', 'meal_type', 'food_name', 'meal_serving')

class UsermealevluationAdmin(admin.ModelAdmin):
    model = Usermealevaluation
    list_display = ('uuid', 'meal_date', 'meal_evaluation')
    
class NutrientAdmin(admin.ModelAdmin):
    model = Nutrient
    list_display = ('food_name', 'weight_g','energy_kcal', 'carbs_g', 
    'sugar_g', 'fat_g', 'protein_g', 'nat_mg','col_mg')

# admin.site.register(CustomUser)
admin.site.register(Nutrient,NutrientAdmin)
admin.site.register(Usermeal,UsermealAdmin)
admin.site.register(Usermealevaluation,UsermealevluationAdmin)
# Register your models here.


    