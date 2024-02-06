# Generated by Django 4.2.8 on 2024-02-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_event_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.CharField(
                choices=[
                    ("music", "Music"),
                    ("games", "Games"),
                    ("sports", "Sports"),
                    ("arts", "Arts"),
                    ("film", "Film"),
                    ("literature", "Literature"),
                    ("technology", "Technology"),
                    ("fashion", "Fashion"),
                    ("lifestyle", "Lifestyle"),
                    ("other", "Other"),
                ],
                default="other",
                max_length=10,
            ),
        ),
    ]