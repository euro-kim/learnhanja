# Generated by Django 5.0.6 on 2024-07-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_0", "0008_alter_model_hanja_meaning_sound_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="model_hanja",
            name="component_sound",
            field=models.CharField(default="一", max_length=10),
        ),
    ]
