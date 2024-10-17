# Generated by Django 5.1.1 on 2024-10-17 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('total_price', models.IntegerField()),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.caretaker')),
                ('pet_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.owner')),
            ],
        ),
    ]