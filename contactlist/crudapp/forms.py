from django import forms
from crudapp.models import Contact, Address, Phone, Date


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        # fields = ['fname','mname','lname']
        fields = "__all__"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address_type", "address", "city", "state", "zipcode"]
        # fields = "__all__"


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = "__all__"
        # fields = ['phone_type','area_code','number']


class DateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        # fields = ['date_type','date']
