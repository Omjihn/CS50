# Generated by Django 4.2.11 on 2024-08-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.URLField(max_length=2048),
        ),
    ]
