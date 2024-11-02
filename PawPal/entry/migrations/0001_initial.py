# Generated by Django 5.1.1 on 2024-11-02 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=59)),
                ('email', models.EmailField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
