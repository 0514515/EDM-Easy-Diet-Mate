# Generated by Django 4.2 on 2024-01-02 04:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_privacypolicy_user_agreed_to_privacy_policy_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="active_level",
            field=models.CharField(
                choices=[
                    ("1", "1레벨 - 주 2회 미만, 움직임 거의 없는 사무직"),
                    ("2", "2레벨 - 주 3~4회 이하, 움직임 조금 있는 직종"),
                    ("3", "3레벨 - 주 5회 이하, 운송업 종사자"),
                    ("4", "4레벨 - 주 6회 이상, 인부 혹은 광부"),
                    ("5", "5레벨 - 운동 선수"),
                ],
                default="level 1",
                max_length=7,
            ),
        ),
    ]
