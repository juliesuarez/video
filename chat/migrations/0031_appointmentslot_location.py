# Generated by Django 3.2.19 on 2023-10-18 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0030_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentslot',
            name='location',
            field=models.CharField(choices=[('Makerere University School of Psychology', 'Makerere University School of Psychology'), ('Makerere University School of Guidance & Counselling', 'Makerere University School of Guidance & Counselling'), ('Safe Places – Kyambogo', 'Safe Places – Kyambogo'), ('Makerere University Business School', 'Makerere University Business School')], default=False, max_length=100),
        ),
    ]
