# Generated by Django 5.0.6 on 2024-06-08 22:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feeds", "0006_alter_post_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.CharField(
                db_index=True,
                default="46d78dca9ffd432dbbdff53430d79bfa",
                editable=False,
                max_length=128,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
