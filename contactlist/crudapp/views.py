from django.db.models import Q, Max
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from crudapp import forms
from crudapp.models import *
from crudapp.forms import ContactForm, AddressForm, PhoneForm, DateForm
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt


# Create your views here.

def listView(request):
    x = request.GET.get('search')

    if request.GET.get('search') == None or request.GET.get('search') == '':
        contacts = Contact.objects.all()
    else:
        contacts = []
        cont_id = []
        if(x.isnumeric()):
            contact_set = Contact.objects.filter(Q(id__icontains=x) | Q(fname__icontains=x) | Q(mname__icontains=x) | Q(lname__icontains=x))
            address_set = Address.objects.filter(

                Q(address__icontains=x) | 
                Q(address_type__icontains=x) |
                Q(city__icontains=x) |
                Q(state__icontains=x) |
                Q(zipcode__icontains=x)
            )
            phone_set = Phone.objects.filter(
                # Q(phone_type_icontains = x) |
                Q(area_code__icontains=int(x)) |
                Q(number__icontains=int(x))
            )
            date_set = Date.objects.filter(
                Q(date_type__icontains=x) |
                Q(date__regex=x)
            )

            for cont in contact_set:
                cont_id.append(cont.id)
            for adder in address_set:
                cont_id.append(adder.contact_id)
            for phon in phone_set:
                cont_id.append(phon.contact_id)
            for dat in date_set:
                cont_id.append(dat.contact_id)

            print(contact_set)
            print(address_set)
            print(phone_set)
            print(date_set)

        else:
            contact_set = Contact.objects.filter(
                Q(fname__contains=x) |
                Q(mname__contains=x) |
                Q(lname__contains=x)
            )
            address_set = Address.objects.filter(
                Q(address__contains=x) |
                Q(address_type=x) |
                Q(city__contains=x) |
                Q(state__contains=x)
            )

            phone_set = Phone.objects.filter(
                Q(phone_type__icontains=x)
                # Q(area_code__icontains = int(x)) |
                # Q(number__icontains = int(x))
            )

            date_set = Date.objects.filter(
                Q(date_type__icontains=x)
                # Q(date__regex = x)
            )

            for cont in contact_set:
                cont_id.append(cont.id)
            for adder in address_set:
                cont_id.append(adder.contact_id)
            for pho in phone_set:
                cont_id.append(pho.contact_id)
            for dt in date_set:
                cont_id.append(dt.contact_id)

        print(contact_set)
        print(address_set)
        print(phone_set)
        print(date_set)

        cont_id = list(set(cont_id))

        for cont in cont_id:
            contacts.append(Contact.objects.get(id=cont))

    return render(request, "data-list.html", context={'contacts': contacts})


def show(request):
    cform = Contact.objects.all()
    aform = Address.objects.all()
    pform = Phone.objects.all()
    dform = Date.objects.all()

    # context ={
    #             'cform':cform,
    #             'aform':aform,
    #             'pform':pform,
    #             'dform':dform,
    #         }

    context = {
        'ziplist': zip(cform, aform, pform, dform)
    }

    return render(request, 'show.html', context=context)
    # return render(request, 'data-list.html')


# class editView(View):

    def get(self, request, pk):

        cform = Contact.objects.get(pk=pk)
        # aform = Address.objects.filter(contact=cform)
        aform = Address.objects.get(contact=cform)
        pform = Phone.objects.get(contact=cform)
        dform = Date.objects.get(contact=cform)

        # context ={
        #     'ziplist':zip(cform,aform,pform,dform)
        # }

        context = {
            'cform': cform,
            'aform': aform,
            'pform': pform,
            'dform': dform,
        }
        return render(request, 'edit.html', context=context)

    def post(self, request, pk):
        form = request.POST

        fname = form.get('fname')
        mname = form.get('mname')
        lname = form.get('lname')

        # address table

        ad_type = form.get('address_type')
        address = form.get('address')
        city = form.get('city')
        state = form.get('state')
        zipcode = form.get('zipcode')

        # phone table

        phone_type = form.get('phone_type')
        area_code = form.get('area_code')
        number = form.get('phone')

        # date table

        date_type = form.get('date_type')
        date = form.get('date')

        a_obj = Address.objects.get(contact=pk)
        c_obj = Contact.objects.get(pk=a_obj.contact.id)
        p_obj = Phone.objects.get(contact=pk)
        d_obj = Date.objects.get(contact=pk)

        c_obj.fname = fname
        c_obj.mname = mname
        c_obj.lname = lname

        c_obj.save()

        a_obj.address_type = ad_type
        a_obj.address = address
        a_obj.city = city
        a_obj.state = state
        a_obj.zipcode = zipcode

        a_obj.save()

        p_obj.phone_type = phone_type
        p_obj.phone = number
        p_obj.area_code = area_code

        p_obj.save()

        d_obj.date_type = date_type
        d_obj.date = date

        d_obj.save()

        return redirect('/search')


class updateView(View):
    def get(self, request, pk):
        address = Address.objects.filter(contact=pk)
        contact = Contact.objects.get(pk=pk)
        phone = Phone.objects.filter(contact=pk)
        date = Date.objects.filter(contact=pk)

        context = {
            'cform': contact,
            'aform': address,
            'pform': phone,
            'dform': date,
        }

        return render(request, 'update.html', context)

    def post(self, request, pk):

        form = request.POST

        address = Address.objects.filter(contact=pk)
        contact = Contact.objects.get(pk=pk)
        phone = Phone.objects.filter(contact=pk)
        date = Date.objects.filter(contact=pk)

        context = {
            'cform': contact,
            'aform': address,
            'pform': phone,
            'dform': date,
        }

        address_id = []
        phone_id = []
        date_id = []

        # get all ids of all table
        for ad in address:
            address_id.append(ad.id)

        for ph in phone:
            phone_id.append(ph.id)

        for d in date:
            date_id.append(d.id)

        contact.fname = form.get('fname')
        contact.mname = form.get('mname')
        contact.lname = form.get('lname')

        contact.save()

        address_types = form.getlist('address_type')
        addresses = form.getlist('address')
        cities = form.getlist('city')
        states = form.getlist('state')
        zipcodes = form.getlist('zipcode')

        # phone table
        phone_types = form.getlist('phone_type')
        area_codes = form.getlist('area_code')
        numbers = form.getlist('phone')

        # date table
        date_types = form.getlist('date_type')
        dates = form.getlist('date')

        i, j = 0, 0
        if len(address) >= len(address_types):
            for i in range(len(address)):
                if address_types[i] != '' or address_types != None:
                    address[i].address_type = address_types[i]
                address[i].address = addresses[i]
                address[i].city = cities[i]
                address[i].state = states[i]
                address[i].zipcode = zipcodes[i]
                j = i
                if address_types[i] == 'delete':
                    address[i].delete()
                    continue
                address[i].save()
        else:
            # for j in range(len(address_types)):
            # if address_types[i] =='':
            #     address_types[i] = None
            # if numbers[i] == '':
            #     numbers[i] = None
            flag = False
            if (address_types[i] == 'Select' or address_types[i] == '') and cities[i] == '' and states[i] == '' and zipcodes[i] == '':
                flag = True

            if addresses[i] == '':
                addresses[i] = None
            if cities[i] == '':
                cities[i] = None
            if states[i] == '':
                states[i] = None
            if zipcodes[i] == '':
                zipcodes[i] = 99999

            if flag == False:
                Address.objects.create(
                    contact_id=pk,
                    address_type=address_types[-1],
                    address=addresses[-1],
                    city=cities[-1],
                    state=states[-1],
                    zipcode=zipcodes[-1]
                )
        i = 0
        if len(phone) >= len(phone_types):
            for i in range(len(phone)):
                if phone_types[i] != '' or phone_types != None:
                    phone[i].phone_type = phone_types[i]
                phone[i].area_code = area_codes[i]
                phone[i].number = numbers[i]
                if phone_types[i] == 'delete':
                    phone[i].delete()
                    print("deleted")
                    continue
                phone[i].save()
        else:
            if area_codes[i] == '':
                area_codes[i] = 111
            if numbers[i] == '':
                numbers[i] = None
            Phone.objects.create(
                contact_id=pk,
                phone_type=phone_types[-1],
                area_code=area_codes[-1],
                number=numbers[-1]
            )
        i = 0
        if len(date) >= len(date_types):
            for i in range(len(date)):
                if date_types[i] != '':
                    date[i].date_type = date_types[i]
                if dates[i] != '':
                    date[i].date = dates[i]
                if date_types[i] == 'delete':
                    date[i].delete()
                    continue
                date[i].save()
        else:
            if dates[i] == '':
                dates[i] = None
            Date.objects.create(
                contact_id=pk,
                date_type=date_types[-1],
                date=dates[-1]
            )

        return redirect('/search')


class insertView(View):

    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):

        print(request.POST)
        form = request.POST
        # contact values

        fname = form.get('fname')
        mname = form.get('mname')
        lname = form.get('lname')

        # address table

        address_type = form.getlist('address_type')
        address = form.getlist('address')
        city = form.getlist('city')
        state = form.getlist('state')
        zipcode = form.getlist('zipcode')

        # phone table

        phone_type = form.getlist('phone_type')
        area_code = form.getlist('area_code')
        number = form.getlist('phone')

        # date table

        date_type = form.getlist('date_type')
        date = form.getlist('date')

        cid = Contact.objects.create(
            fname=fname,
            mname=mname,
            lname=lname,
        )
        # cid = Contact.objects.last().id
        # cid = Contact.objects.all().aggregate(Max('id'))
        # cid = cid['id__max']
        print("cid: ", cid)
        n = len(address_type)

        for i in range(n):
            if (address_type[i] == 'Select' or address_type[i] == '') and address[i] == '' and city[i] == '' and state[i] == '' and zipcode[i] == '':
                continue
            if address[i] == '':
                address[i] = None
            if city[i] == '':
                city[i] = None
            if state[i] == '':
                state[i] = None
            if zipcode[i] == '':
                zipcode[i] = 10000

            Address.objects.create(
                contact=cid,
                address_type=address_type[i],
                address=address[i],
                city=city[i],
                state=state[i],
                zipcode=zipcode[i]
            )

        n = len(phone_type)

        for i in range(n):
            if phone_type[i] == 'Select' and area_code[i] == '' and number == '':
                continue
            if area_code[i] == '':
                area_code[i] = None
            if number[i] == '':
                number[i] = None
            Phone.objects.create(
                contact=cid,
                phone_type=phone_type[i],
                area_code=area_code[i],
                number=number[i]
            )

        n = len(date_type)

        for i in range(n):
            if date_type[i] == 'Select' and date[i] == '':
                continue
            if date[i] == '':
                date[i] = None
            Date.objects.create(
                contact=cid,
                date_type=date_type[i],
                date=date[i]
            )

        return redirect('/search')


class deleteView(View):

    def get(self, request, pk):
        cont_obj = Contact.objects.get(pk=pk)
        cont_obj.delete()

        return redirect('/search')
