# Generated by Django 3.2.19 on 2023-09-22 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_message_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
