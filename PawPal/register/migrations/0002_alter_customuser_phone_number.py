# Generated by Django 5.1.1 on 2024-10-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
    ]