# Generated by Django 3.2.19 on 2023-10-22 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0039_auto_20231019_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentslot',
            name='conditions',
        ),
        migrations.DeleteModel(
            name='MentalHealthCondition',
        ),
    ]