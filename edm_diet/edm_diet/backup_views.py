# def get_nutrient(food_name):
#     print(food_name) # Nutrient object (쌀밥)
#     try:
#         nutrient = Nutrient.objects.get(food_name = food_name)
#         return {
#             'carbs': nutrient.carbs_g,
#             'protein': nutrient.protein_g,
#             'fat': nutrient.fat_g,
#             'sugar': nutrient.sugar_g, 
#         }
#     except Usermeal.DoesNotExist:
#         raise Http404("Usermeal does not exist")

# def get_nutrient(food_name):
#     food_name.carbs_g
#     nutrients = Nutrient.objects.filter(food_name=food_name)
#     if nutrients.exists():
#         nutrient = nutrients.first()
#         return {
#             'carbs': nutrient.carbs_g,
#             'protein': nutrient.protein_g,
#             'fat': nutrient.fat_g,
#             'sugar': nutrient.sugar_g, 
#         }
#     else:
#         print("Error: None Data") # 여기에 데이터를 db에 추가하여 저장하는 코드 작성
#         return None