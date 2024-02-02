# Generated by Django 4.2.8 on 2024-02-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_ticket_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_status',
            field=models.CharField(choices=[('success', 'Success'), ('fail', 'Fail'), ('cancelled', 'Cancelled')], default='fail', max_length=20),
        ),
    ]