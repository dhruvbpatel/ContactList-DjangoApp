from django.db.models import Q,Max
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from crudapp import forms
from crudapp.models import *
from crudapp.forms import ContactForm,AddressForm,PhoneForm,DateForm
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from dateutil import parser


# Create your views here.


def show(request):
    cform =Contact.objects.all()
    aform = Address.objects.all()
    pform = Phone.objects.all()
    dform = Date.objects.all()
    
    # context ={
    #             'cform':cform,
    #             'aform':aform,
    #             'pform':pform,
    #             'dform':dform,
    #         }
    
    context ={
        'ziplist': zip(cform, aform, pform, dform)
    }

    return render(request, 'show.html', context=context)
    # return render(request, 'data-list.html')
    

class ContactList(View):
    
    template_name = 'data-list.html'

    def get(self, request, *args, **kwargs):


        context = {}
        return render(request, self.template_name, context)


@csrf_exempt
def data_list_table(request):
    if request.method == 'POST':
        form = request.POST
        first_name = form.get('first_name')
        last_name = form.get('last_name')
        number = form.get('number')
        address = form.get('address')
        date = form.get('date')

        # particular column for datatable list
        column_dict = {0: 'id', 1: 'first_name', 2: 'middle_name', 3: 'last_name', 4: 'last_name',
                       5: 'address_type', 6: 'address', 7: 'city', 8: 'state', 9: 'zipcode',
                       10: 'phone_type', 11: 'area_code', 12: 'number', 13: 'date_type', 14: 'date'}

        filters = Q()
        if address:
            
            filters = filters & Q(addresscontact__address__icontains=address)
        if first_name:
            filters = filters & Q(fname__icontains=first_name)
            # Contact.objects.filter(filter)

        if last_name:
            filters = filters & Q(lname__icontains=last_name)
        if number:
            filters = filters & Q(phonecontact__number__icontains=number)
        c_form = Contact.objects.all()
        # if first_name:
        #     c_form = Contact.objects.filter(Q(addresscontact_icontains=first_name) |
        #                                 Q(datecontact__icontains=first_name) |
        #                                 Q(Contact__icontains=first_name) |
        #                                 Q(phonecontact_icontains=first_name))

        c_form = Contact.objects.filter(filters)
        print(f" >>>  {c_form}")
        print(f" >>>  {c_form.query}")

        # a_form = Address.objects.filter(filters)
        # p_form = Phone.objects.filter(filters)
        # d_form = Date.objects.filter(filters)

        data_list = [
            [
                c.pk,
                c.fname,
                c.mname,
                c.lname,
                Address.objects.get(contact_id=c.pk).address_type,
                Address.objects.get(contact_id=c.pk).address,
                Address.objects.get(contact_id=c.pk).city,
                Address.objects.get(contact_id=c.pk).state,
                Address.objects.get(contact_id=c.pk).zipcode,
                Phone.objects.get(contact_id=c.pk).phone_type,
                Phone.objects.get(contact_id=c.pk).area_code,
                Phone.objects.get(contact_id=c.pk).number,
                Date.objects.get(contact_id=c.pk).date_type,
                Date.objects.get(contact_id=c.pk).date

            ] for c in c_form
        ]

        # data_list = [
        #     [
        #         c.pk,
        #         c.fname,
        #         c.mname,
        #         c.lname,
        #         a.address_type,
        #         a.address,
        #         a.city,
        #         a.state,
        #         a.zipcode,
        #         p.phone_type,
        #         p.area_code,
        #         p.number,
        #         d.date_type,
        #         d.date
        #
        #     ] for c, a, p, d in zip(c_form, a_form, p_form, d_form)
        # ]

        context = {
            'data': data_list
        }
        return JsonResponse(context)



class editView(View):

    def get(self, request,pk):

        cform =Contact.objects.get(pk=pk)
        # aform = Address.objects.filter(contact=cform)
        aform = Address.objects.get(contact=cform)
        pform = Phone.objects.get(contact=cform)
        dform = Date.objects.get(contact=cform)


        # context ={ 
        #     'ziplist':zip(cform,aform,pform,dform)
        # }

        context ={
                'cform':cform,
                'aform':aform,
                'pform':pform,
                'dform':dform,
            }
        return render(request, 'edit.html',context=context)

    def post(self, request,pk):
        form = request.POST

        fname = form.get('fname')
        mname = form.get('mname')
        lname = form.get('lname')

        # address table

        ad_type = form.get('address_type')
        address = form.get('address')
        city  = form.get('city')
        state = form.get('state')
        zipcode = form.get('zipcode')


        #phone table

        phone_type = form.get('phone_type')
        area_code = form.get('area_code')
        number = form.get('phone')


        #date table

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


        return redirect('/show')

class updateView(View):
    def get(self,request,pk):
        address = Address.objects.filter(contact=pk)
        contact = Contact.objects.get(pk=pk)
        phone = Phone.objects.filter(contact=pk)
        date = Date.objects.filter(contact=pk)

        context ={
                'cform':contact,
                'aform':address,
                'pform':phone,
                'dform':date,
            }
        
        return render(request,'update.html',context)


    def post(self,request,pk):

        form = request.POST

        address = Address.objects.filter(contact=pk)
        contact = Contact.objects.get(pk=pk)
        phone = Phone.objects.filter(contact=pk)
        date = Date.objects.filter(contact=pk)

        context ={
                'cform':contact,
                'aform':address,
                'pform':phone,
                'dform':date,
            }
        
        address_id= []
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
        cities  = form.getlist('city')
        states = form.getlist('state')
        zipcodes = form.getlist('zipcode')

        #phone table
        phone_types = form.getlist('phone_type')
        area_codes = form.getlist('area_code')
        numbers = form.getlist('phone')


        #date table
        date_types = form.getlist('date_type')
        dates = form.getlist('date')

    
        i,j  = 0,0
        if len(address)>=len(address_types):
            for i in range(len(address)):
                if address_types[i] != '' or address_types != None:
                    address[i].address_type = address_types[i]
                address[i].address = addresses[i]
                address[i].city = cities[i]
                address[i].state = states[i]
                address[i].zipcode = zipcodes[i]
                j=i
                if address_types[i]=='Delete':
                    address[i].delete()
                    continue
                address[i].save()
        else:
            # for j in range(len(address_types)):
            # if address_types[i] =='':
            #     address_types[i] = None
            # if numbers[i] == '':
            #     numbers[i] = None
            if addresses[i] == '':
                addresses[i] = None
            if cities[i] == '':
                cities[i] = None
            if states[i] == '':
                states[i] = None
            if zipcodes[i] =='':
                zipcodes[i] = None
            
            Address.objects.create(
                    contact_id = pk,
                    address_type = address_types[-1],
                    address=addresses[-1],
                    city = cities[-1],
                    state = states[-1],
                    zipcode = zipcodes[-1]
                )
        i=0
        if len(phone)>=len(phone_types):
            for i in range (len(phone)):
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
            if area_codes[i] =='':
                area_codes[i] = None
            if numbers[i] == '':
                numbers[i] = None
            Phone.objects.create(
                contact_id= pk, 
                phone_type = phone_types[-1],
                area_code = area_codes[-1],
                number = numbers[-1]
                )
        i=0
        if len(date)>=len(date_types):
            for i in range (len(date)):
                if date_types[i] != '':
                    date[i].date_type = date_types[i]
                if dates[i] != '':
                    date[i].date = dates[i]
                if date_types[i] == 'delete':
                    date[i].delete()
                    continue
                date[i].save()
        else:
            if dates[i]=='':
                dates[i]=None
            Date.objects.create(
                contact_id = pk,
                date_type = date_types[-1],
                date = dates[-1]
                )

        return redirect('/')
        



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
        city  = form.getlist('city')
        state = form.getlist('state')
        zipcode = form.getlist('zipcode')


        #phone table

        phone_type = form.getlist('phone_type')
        area_code = form.getlist('area_code')
        number = form.getlist('phone')


        #date table

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
        print("cid: ",cid)
        n = len(address_type)
        
        for i in range(n):
            if address_type[i] =='Select' and address[i]=='' and city[i] =='' and state[i] =='' and zipcode[i]== '':
                continue
            if address[i] == '':
                address[i] = None
            if city[i] == '':
                city[i] = None
            if state[i] == '':
                state[i] = None
            if zipcode[i] == '':
                zipcode[i] = None

            Address.objects.create(
            contact = cid,
            address_type = address_type[i],
            address = address[i],
            city = city[i],
            state = state[i],
            zipcode = zipcode[i]
        )

        n = len(phone_type)

        for i in range(n):
            if phone_type[i] =='Select' and area_code[i]=='' and number=='':
                continue
            if area_code[i]=='':
                area_code[i]=None
            if number[i]=='':
                number[i]=None
            Phone.objects.create(
            contact = cid,
            phone_type = phone_type[i],
            area_code = area_code[i],
            number = number[i]
            )

        n = len(date_type)

        for i in range(n):
            if date_type[i]=='Select' and date[i]=='':
                continue
            if date[i]=='':
                date[i]= None
            Date.objects.create(
                contact = cid,
                date_type = date_type[i],
                date = date[i]
            )

        return redirect('/show')



class deleteView(View):

    def get(self,request,pk):
        cont_obj = Contact.objects.get(pk=pk)
        cont_obj.delete()

        return redirect('/show')










        

















