# Generated by Django 3.2.7 on 2021-09-22 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineProjectApproval', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='id',
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
