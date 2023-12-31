# Generated by Django 4.2.8 on 2023-12-20 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "PID",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("success", "Success"),
                            ("fail", "Fail"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=10,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tickets.ticket"
                    ),
                ),
            ],
        ),
    ]
