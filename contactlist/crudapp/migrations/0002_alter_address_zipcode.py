# Generated by Django 3.2.9 on 2021-11-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
    ]