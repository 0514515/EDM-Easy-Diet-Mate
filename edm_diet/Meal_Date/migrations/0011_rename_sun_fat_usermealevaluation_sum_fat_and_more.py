# Generated by Django 4.2 on 2024-01-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Meal_Date", "0010_remove_usermealevaluation_sys_config"),
    ]

    operations = [
        migrations.RenameField(
            model_name="usermealevaluation",
            old_name="sun_fat",
            new_name="sum_fat",
        ),
        migrations.AddField(
            model_name="usermealevaluation",
            name="sum_kcal",
            field=models.FloatField(blank=True, null=True),
        ),
    ]