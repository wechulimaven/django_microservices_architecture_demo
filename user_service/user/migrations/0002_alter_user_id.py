# Generated by Django 5.0.6 on 2024-06-04 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.CharField(
                db_index=True,
                default="c9191daebf0e4e0c9c907f1ba24296af",
                editable=False,
                max_length=128,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
