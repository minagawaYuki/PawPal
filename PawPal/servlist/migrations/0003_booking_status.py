# Generated by Django 5.1.1 on 2024-11-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servlist', '0002_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
