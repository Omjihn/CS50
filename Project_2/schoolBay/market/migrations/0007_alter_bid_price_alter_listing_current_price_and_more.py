# Generated by Django 4.2.11 on 2024-07-23 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_listing_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=24),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=24),
        ),
    ]
