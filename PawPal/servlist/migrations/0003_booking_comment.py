# Generated by Django 5.1.1 on 2024-11-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servlist', '0002_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
