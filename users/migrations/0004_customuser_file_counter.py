# Generated by Django 4.2.4 on 2023-08-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_uploadedfile_shared_with_alter_uploadedfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='file_counter',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
