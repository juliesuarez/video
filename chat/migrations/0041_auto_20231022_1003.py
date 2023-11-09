# Generated by Django 3.2.19 on 2023-10-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0040_auto_20231022_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentalHealthCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='appointmentslot',
            name='conditions',
            field=models.ManyToManyField(to='chat.MentalHealthCondition'),
        ),
    ]
