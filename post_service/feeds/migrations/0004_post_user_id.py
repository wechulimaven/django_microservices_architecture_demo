# Generated by Django 5.0.6 on 2024-06-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feeds", "0003_post_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="user_id",
            field=models.CharField(
                default="2d3ceefdc2cd4331ba0fd9dd3fc3e3e8", max_length=100
            ),
        ),
    ]
