# Generated by Django 5.0.6 on 2024-07-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_0", "0006_alter_model_hanja_explanation_alter_model_hanja_form"),
    ]

    operations = [
        migrations.AlterField(
            model_name="model_hanja",
            name="meaning",
            field=models.TextField(default="하나"),
        ),
    ]
