# Generated by Django 4.2.8 on 2024-01-17 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="duration",
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]
