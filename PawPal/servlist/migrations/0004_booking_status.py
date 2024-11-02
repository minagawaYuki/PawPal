# Generated by Django 5.1.1 on 2024-11-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servlist', '0003_booking_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Finished', 'Finished'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]
