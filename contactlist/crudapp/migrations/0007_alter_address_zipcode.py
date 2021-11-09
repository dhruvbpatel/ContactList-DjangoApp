# Generated by Django 3.2.9 on 2021-11-08 20:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crudapp", "0006_alter_address_zipcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="zipcode",
            field=models.BigIntegerField(
                blank=True,
                default=99999,
                max_length=5,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(10000),
                    django.core.validators.MaxValueValidator(99999),
                ],
            ),
        ),
    ]
