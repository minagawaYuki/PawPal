# Generated by Django 5.1.1 on 2024-12-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servlist', '0014_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(default=1, max_length=255),
        ),
    ]