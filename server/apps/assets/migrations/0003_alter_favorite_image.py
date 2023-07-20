# Generated by Django 4.1.7 on 2023-07-20 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0002_alter_favorite_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="image",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite",
                to="assets.image",
            ),
        ),
    ]
