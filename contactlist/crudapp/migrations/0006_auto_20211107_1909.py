# Generated by Django 3.2.9 on 2021-11-08 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0005_alter_address_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(blank=True, choices=[('home', 'home'), ('work', 'work'), ('other', 'other')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='phone_type',
            field=models.CharField(choices=[('home', 'home'), ('work', 'work'), ('other', 'other')], max_length=20, null=True),
        ),
    ]