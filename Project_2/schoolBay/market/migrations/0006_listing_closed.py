# Generated by Django 4.2.11 on 2024-07-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_listing_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]