# Generated by Django 5.0.6 on 2024-07-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_0", "0005_model_hanja_origin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="model_hanja",
            name="explanation",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="model_hanja",
            name="form",
            field=models.CharField(default="", max_length=10),
        ),
    ]
