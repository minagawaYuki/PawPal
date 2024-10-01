# Generated by Django 5.1.1 on 2024-09-30 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=100)),
                ('pet_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services', models.CharField(choices=[('Pet Boarding', 'Pet Boarding'), ('Pet Grooming', 'Pet Grooming'), ('Pet Walking', 'Pet Walking')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servlist.pet')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servlist.service')),
            ],
        ),
    ]
