# Generated by Django 4.2.8 on 2024-02-09 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_info', '0004_alter_appointment_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='state',
            field=models.CharField(default='booked', max_length=16),
        ),
    ]
