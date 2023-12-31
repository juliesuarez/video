# Generated by Django 3.2.19 on 2023-09-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_userprofile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_organization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='organization_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='representative_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
