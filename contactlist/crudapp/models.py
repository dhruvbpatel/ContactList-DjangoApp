from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.


class Contact(models.Model):
    # contact = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100)

    class Meta:
        db_table = "contact"

    # def __str__(self):
    #     return self.pk


class Address(models.Model):

    address_choice = [("home", "home"), ("work", "work"), ("other", "other")]

    # address_id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="addresscontact"
    )
    address_type = models.CharField(
        choices=address_choice, blank=True, null=True, max_length=20
    )
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.BigIntegerField(
        max_length=5,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)],
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "address"

    # def __str__(self):
    #     return self.pk


class Phone(models.Model):

    phone_choices = [("home", "home"), ("work", "work"), ("other", "other")]
    # phone_id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="phonecontact"
    )
    phone_type = models.CharField(
        choices=phone_choices, null=True, blank=True, max_length=20
    )
    area_code = models.BigIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        blank=True,
        null=True,
    )
    number = models.BigIntegerField(
        validators=[MinValueValidator(1000000), MaxValueValidator(9999999)],
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "phone"

    # def __str__(self):
    #     return self.pk


class Date(models.Model):

    date_choices = [
        ("birthday", "birthday"),
        ("aniversary", "aniversary"),
        ("other", "other")
        # ('SR', 'Senior'),
        # ('GR', 'Graduate'),
    ]

    # date_id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="datecontact"
    )
    date_type = models.CharField(choices=date_choices, null=True, max_length=21)
    date = models.DateField(null=True)

    class Meta:
        db_table = "date"

    # def __str__(self):
    #     return self.pk
