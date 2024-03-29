# Generated by Django 4.2.9 on 2024-02-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0006_alter_ticket_ticket_status"),
    ]

    operations = [
        migrations.RemoveField(model_name="ticket", name="attending",),
        migrations.AlterField(
            model_name="ticket",
            name="ticket_status",
            field=models.CharField(
                choices=[
                    ("success", "Success"),
                    ("not_paid", "Not Paid"),
                    ("fail", "Fail"),
                    ("cancelled", "Cancelled"),
                ],
                default="not_paid",
                max_length=20,
            ),
        ),
    ]
