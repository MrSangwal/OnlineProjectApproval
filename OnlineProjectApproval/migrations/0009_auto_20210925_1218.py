# Generated by Django 3.2.7 on 2021-09-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineProjectApproval', '0008_auto_20210925_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Pic',
            field=models.FileField(null=True, upload_to='media/images'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='Pic',
            field=models.FileField(null=True, upload_to='media/images'),
        ),
    ]
