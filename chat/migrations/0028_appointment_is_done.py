# Generated by Django 3.2.19 on 2023-10-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
