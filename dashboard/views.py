from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime, timezone
from django.contrib import messages
from .models import Payment, Unit,Feed, Apartment, status
from django.db.models import Count
from user.models import Tenant, Landlord, User, Agent
from .form import unitForm, unitUpdateForm, apartmentForm, agentapartmentForm
from user.forms import TenantcreateForm
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='user-login')
def index(request): 
    current_month = datetime.now().month
    current_year = datetime.now().year
    if request.user.is_authenticated:
    

        if request.user.groups.filter(name='Agent').exists():  
        
            return redirect('dashboard-agent-index') 
        
        elif request.user.groups.filter(name='Landlord').exists():
            
            return redirect('dashboard-landlord-index') 
        
            
        items = Unit.objects.filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference')) 
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()

        unit = Unit.objects.all()
        unit_count = unit.count()
        feeds = Feed.objects.all()
        payment = Payment.objects.filter(accountReference__in=items.values('door_no'))
        counts = Unit.objects.values('Rent_status').annotate(count=Count('Rent_status'))
        
        Expected_Amount = unit.aggregate(Sum('rent'))['rent__sum'] or 0
        receipt_paid = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=unit.values('door_no'))
        Paid_Amount = receipt_paid.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
        jo = Paid_Amount / Expected_Amount
        progress = round(jo * 100)

        context  ={
                'progress':progress,
                'unit':unit,
                'counts':counts,
                'unit_count':unit_count,
                'payment':payment,
                "feeds":feeds,
            }

        return render(request,'dashboard/index.html', context) 


@login_required
def agent_index(request):

        agent = Agent.objects.get(name = request.user)
        apartments = Apartment.objects.filter(agent=agent)
        landlords = Landlord.objects.filter(agent=agent)   
        current_month = datetime.now().month
        current_year = datetime.now().year      

        items = Unit.objects.filter(apartment__in=apartments).filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference')) 
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()

        landlord_data = []  
        for ld in landlords:
                landlord1 = Landlord.objects.get(name = ld.name)
                apts = Apartment.objects.filter(landlord=landlord1)
                No_Apts = apts.count()
                units = Unit.objects.filter(apartment__in=apts)
                Units_count = units.count()
                tenants = Tenant.objects.filter(landlord=landlord1)
                Tenants_count = tenants.count()
                Expected_Amount = units.aggregate(Sum('rent'))['rent__sum'] or 0
                tenant_paid = units.filter(Rent_status = 'Paid')
                Paid_Tenants = tenant_paid.count()
                receipt_paid = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=units.values('door_no'))
                Paid_Amount = receipt_paid.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
                #Deficit_Amount = Expected_Amount - Paid_Amount if (Expected_Amount and Paid_Amount) else 0
                in_arrs = units.exclude(hse_status = 'Empty').exclude(Rent_status = 'Paid')
                Not_Paid_Tenants = in_arrs.count()
                Deficit_Amount = in_arrs.aggregate(Sum('rent'))['rent__sum'] or 0
                landlord_data.append({
                    'Landlord':landlord1,
                    'apartment_count':No_Apts,
                    'unit_count':Units_count,
                    'Tenants_count': Tenants_count,
                    'Expected_Amount': Expected_Amount,
                    'Paid_Tenants':Paid_Tenants,
                    'Paid_Amount': Paid_Amount,
                    'Deficit_Amount': Deficit_Amount,
                    'Not_Paid_Tenants': Not_Paid_Tenants,
                })


        monthly_payments = Payment.objects.annotate(month=TruncMonth('paymentDate')
        ).values('month').annotate(total_paid=Sum('paidAmount')).order_by('month')

        feeds = Feed.objects.all()
        unit = Unit.objects.filter(apartment__in=apartments)
        payment = Payment.objects.filter(accountReference__in=items.values('door_no'))
        counts = Unit.objects.filter(apartment__in=apartments).values('Rent_status').annotate(count=Count('Rent_status'))
        Expected_Amount = unit.aggregate(Sum('rent'))['rent__sum'] or 0
        receipt_paid = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=unit.values('door_no'))
        Paid_Amount = receipt_paid.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
        jo = Paid_Amount / Expected_Amount
        paid = round(jo * 100)
        arrears = 100 - paid
        arr = Expected_Amount - Paid_Amount
        context  ={
            'monthly_payments':monthly_payments,
            'Expected_Amount':Expected_Amount,
            'landlord_data':landlord_data,  
            'counts':counts,
            'arr':arr,
            'Expected_Amount':Expected_Amount,
            'Paid_Amount':Paid_Amount,
            'arrears':arrears,
            'paid':paid,
            'unit':unit,
            'payment':payment,
            "feeds":feeds,
        }

        return render(request,'dashboard/agent_index.html', context)

@login_required
def landlord_index(request):
        current_month = datetime.now().month
        current_year = datetime.now().year
        landlord = Landlord.objects.get(name = request.user)
        apartments = Apartment.objects.filter(landlord=landlord)
        items = Unit.objects.filter(apartment__in=apartments).filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference')) 
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()

        apt_data = []
        for apt in apartments:
                apt1 = Apartment.objects.get(name = apt.name)
                units = Unit.objects.filter(apartment=apt)
                Units_count = units.count()
                tenants = units.filter(tenant__isnull=False)
                Tenants_count = tenants.count()
                Expected_Amount = units.aggregate(Sum('rent'))['rent__sum'] or 0
                tenant_paid = units.filter(Rent_status = 'Paid')
                Paid_Tenants = tenant_paid.count()
                receipt_paid = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=units.values('door_no'))
                Paid_Amount = receipt_paid.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
                Deficit_Amount = Expected_Amount - Paid_Amount if (Expected_Amount and Paid_Amount) else 0
                Not_Paid_Tenants = units.exclude(hse_status = 'Empty').exclude(Rent_status = 'Paid').count()
                apt_data.append({
                    'apartment_name':apt1,
                    'unit_count':Units_count,
                    'Tenants_count': Tenants_count,
                    'Expected_Amount': Expected_Amount,
                    'Paid_Tenants':Paid_Tenants,
                    'Paid_Amount': Paid_Amount,
                    'Deficit_Amount': Deficit_Amount,
                    'Not_Paid_Tenants': Not_Paid_Tenants,
                })

        monthly_payments = Payment.objects.annotate(month=TruncMonth('paymentDate')
        ).values('month').annotate(total_paid=Sum('paidAmount')).order_by('month')

        unit = Unit.objects.filter(apartment__in=apartments)
        unit_count = unit.count()
        feeds = Feed.objects.all()
        payment = Payment.objects.filter(accountReference__in=items.values('door_no'))
        counts = Unit.objects.filter(apartment__in=apartments).values('Rent_status').annotate(count=Count('Rent_status'))
        Expected_Amount = unit.aggregate(Sum('rent'))['rent__sum'] or 0
        receipt_paid = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=unit.values('door_no'))
        Paid_Amount = receipt_paid.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
        jo = Paid_Amount / Expected_Amount
        paid = round(jo * 100)
        arrears = 100 - paid
        arr = Expected_Amount - Paid_Amount


        context  ={
            'monthly_payments':monthly_payments,
            'arr':arr,
            'Expected_Amount':Expected_Amount,
            'Paid_Amount':Paid_Amount,
            'arrears':arrears,
            'paid':paid,
            'apt_data':apt_data,
            'unit':unit,
            'counts':counts,
            'unit_count':unit_count,
            'payment':payment,
            "feeds":feeds,
        }
        return render(request,'dashboard/landlord_index.html', context)


@login_required(login_url='user-login')
def paid_record(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        apartments = Apartment.objects.filter(landlord=landlord)
        items = Unit.objects.filter(apartment__in=apartments).filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference'))   
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()

        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = items.filter(door_no__contains=search_query)
            return render(request, 'dashboard/paid_record.html', {'query':search_query, 'items':items})
            
        context = {
            'items':items,
        }

        return render (request, 'dashboard/paid_record.html', context )
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        apartments = Apartment.objects.filter(agent=agent)
        
        items = Unit.objects.filter(apartment__in=apartments).filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference'))   
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = items.filter(door_no__contains=search_query)
            return render(request, 'dashboard/paid_record.html', {'query':search_query, 'items':items})

        context = {
          
            'items':items,
        }

        return render (request, 'dashboard/paid_record.html', context )
    else:
        
        items = Unit.objects.filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference'))   
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = items.filter(door_no__contains=search_query)
            return render(request, 'dashboard/paid_record.html', {'query':search_query, 'items':items})  
        context = {
            'items':items,
        }

        return render (request, 'dashboard/paid_record.html', context )
    
@login_required(login_url='user-login')
def paid_tenant(request, landlord):
        current_month = datetime.now().month
        current_year = datetime.now().year
        landlord_obj = Landlord.objects.get(id=landlord)
        apartments = Apartment.objects.filter(landlord=landlord_obj)
        items = Unit.objects.filter(apartment__in=apartments).filter(door_no__in=Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).values('accountReference'))   
        for item in items:
            item.Rent_status = "Paid"
            item.hse_status = "Occupied"
            item.save()

        context = {
          
            'items':items,
        }

        return render (request, 'dashboard/paid_tenant.html', context )

@login_required(login_url='user-login')
def tenant_arrears(request, landlord): 
        landlord_obj = Landlord.objects.get(id=landlord)
        apartments = Apartment.objects.filter(landlord=landlord_obj)
        items = Unit.objects.filter(apartment__in=apartments).exclude(hse_status = 'Empty').exclude(Rent_status = 'Paid')
        context = { 
            'items':items,
        }
        return render (request, 'dashboard/tenant_arrears.html', context )




@login_required(login_url='user-login')
def unit_payment(request, pk):
    paidUnit = Unit.objects.get(id=pk)
    paying_unit = paidUnit.door_no
    receipts = Payment.objects.filter(accountReference__icontains=paying_unit).values


    context = {
        'receipts':receipts,
        'paying_unit':paying_unit,
        'paidUnit': paidUnit,
        
    }

    return render(request, 'dashboard/unit_payment.html', context)

@login_required(login_url='user-login')
def apartment(request, pk):  
        items = Unit.objects.filter(apartment=pk)
        apt_name = Apartment.objects.get(id=pk)

        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = Unit.objects.filter(apartment=pk).filter(door_no__contains=search_query)
            return render(request, 'dashboard/apartment.html', {'query':search_query, 'items':items})
        
        context = {
            'items':items,
            'apt_name':apt_name,
        }
        return render(request, 'dashboard/apartment.html', context)
    


@login_required(login_url='user-login')
def unit_update(request, pk):
    
    item = Unit.objects.get(id=pk) 
    if request.method == 'POST':
        form = unitUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            house_name = form.cleaned_data.get('door_no')
            messages.success(request, f'House No. {house_name} Updated successfully')
            return redirect('dashboard-unit-update', pk = pk)
    else:
        form = unitUpdateForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/unit_update.html', context)

@login_required(login_url='user-login')
def receipt(request):
   
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        apartments = Apartment.objects.filter(landlord=landlord)
        unit = Unit.objects.filter(apartment__in=apartments)
        items = Payment.objects.filter(accountReference__in=unit.values('door_no'))
        
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = Payment.objects.filter(accountReference__in=unit.values('door_no')).filter(accountReference__contains=search_query)
            return render(request, 'dashboard/receipt.html', {'query':search_query, 'items':items})


        context = {
            'items':items,
        }
        return render(request, 'dashboard/receipt.html', context)
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        apartments = Apartment.objects.filter(agent=agent)
        unit = Unit.objects.filter(apartment__in=apartments)
        items = Payment.objects.filter(accountReference__in=unit.values('door_no'))

        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = Payment.objects.filter(accountReference__in=unit.values('door_no')).filter(accountReference__contains=search_query)
            return render(request, 'dashboard/receipt.html', {'query':search_query, 'items':items})

        context = {
            'items':items,
        }
        return render(request, 'dashboard/receipt.html', context)
    else:
        
        items = Payment.objects.all()
        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = Payment.objects.filter(accountReference__in=unit.values('door_no')).filter(accountReference__contains=search_query)
            return render(request, 'dashboard/receipt.html', {'query':search_query, 'items':items})

        context = {
            'items':items,
        }
        return render(request, 'dashboard/receipt.html', context)
    
@login_required(login_url='user-login')
def receipt_landlord(request, landlord):
        current_month = datetime.now().month
        current_year = datetime.now().year
        landlord_obj = Landlord.objects.get(id=landlord)
        apartments = Apartment.objects.filter(landlord = landlord_obj)
        unit = Unit.objects.filter(apartment__in=apartments)
        items = Payment.objects.filter(paymentDate__month=current_month, paymentDate__year=current_year).filter(accountReference__in=unit.values('door_no'))

        if request.method == 'POST':
            # Retrieve the search query entered by the user
            search_query = request.POST['search_query']
            # Filter your model by the search query
            items = Payment.objects.filter(accountReference__in=unit.values('door_no')).filter(accountReference__contains=search_query)
            return render(request, 'dashboard/receipt.html', {'query':search_query, 'items':items})
        context = {
            'items':items,
        }
        return render(request, 'dashboard/receipt_landlord.html', context)
    

@login_required(login_url='user-login')
def flat(request):
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        items  = Apartment.objects.filter(landlord=landlord)

        if request.method == 'POST':
            add_apartment_form = apartmentForm(request.POST)
            if add_apartment_form.is_valid():
                new_apartment = add_apartment_form.save(commit=False)
                new_apartment.landlord = landlord  # set the landlord field on the new apartment
                new_apartment.save()
                apartment_name = add_apartment_form.cleaned_data.get('name')
                messages.success(request, f'{apartment_name} has been added')
                return redirect('dashboard-flat')
        else:
            add_apartment_form = apartmentForm()

    
        context = {
            'items':items,
            'add_apartment_form': add_apartment_form,
        }
        return render(request, 'dashboard/flat.html', context)
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        items  = Apartment.objects.filter(agent=agent)
        if request.method == 'POST':
            add_apartment_form = agentapartmentForm(request.POST)
            if add_apartment_form.is_valid():
                new_apartment = add_apartment_form.save(commit=False)
                new_apartment.agent = agent  # set the landlord field on the new apartment
                new_apartment.save()
                apartment_name = add_apartment_form.cleaned_data.get('name')
                messages.success(request, f'{apartment_name} has been added')
                return redirect('dashboard-flat')
        else:
            add_apartment_form = agentapartmentForm()
        context = {
            'items':items,
            'add_apartment_form': add_apartment_form,
        }
        return render(request, 'dashboard/flat.html', context)
    else:
        items  = Apartment.objects.all()
        if request.method == 'POST':
            add_apartment_form = apartmentForm(request.POST)
            if add_apartment_form.is_valid():
                new_apartment = add_apartment_form.save(commit=False)
                apartment_name = add_apartment_form.cleaned_data.get('name')
                messages.success(request, f'{apartment_name} has been added')
                return redirect('dashboard-flat')
        else:
            add_apartment_form = apartmentForm()
        context = {
            'items':items,
            'add_apartment_form': add_apartment_form,
        }
        return render(request, 'dashboard/flat.html', context)
    
@login_required(login_url='user-login')
def flat_landlord(request, landlord):
        agent = Agent.objects.get(name = request.user) 
        landlord_obj = Landlord.objects.get(id=landlord)
        items  = Apartment.objects.filter(landlord = landlord_obj)
        if request.method == 'POST':
            add_apartment_form = apartmentForm(request.POST)
            if add_apartment_form.is_valid():
                new_apartment = add_apartment_form.save(commit=False)
                new_apartment.agent = agent  # set the landlord field on the new apartment
                new_apartment.landlord = landlord_obj
                new_apartment.save()
                apartment_name = add_apartment_form.cleaned_data.get('name')
                messages.success(request, f'{apartment_name} has been added')
                return redirect('dashboard-flat-landlord', landlord)
        else:
            add_apartment_form = apartmentForm()
        context = {
            'items':items,
            'add_apartment_form': add_apartment_form,
        }
        return render(request, 'dashboard/flat_landlord.html', context)

@login_required(login_url='user-login')
def rental(request):
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        apartments = Apartment.objects.filter(landlord=landlord)
        items = Unit.objects.filter(apartment__in=apartments)
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST or None, user=landlord)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No. {house_name} added successfully')
                return redirect('dashboard-rental')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/rental.html', context)
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        apartments = Apartment.objects.filter(agent=agent)
        items = Unit.objects.filter(apartment__in=apartments)
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No. {house_name} has been added')
                return redirect('dashboard-rental')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/rental.html', context)
    else:
       
        items = Unit.objects.all()
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No. {house_name} has been added')
                return redirect('dashboard-rental')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/rental.html', context)

@login_required(login_url='user-login')
def rental_landlord(request, landlord):
        agent = Agent.objects.get(name = request.user)
        landlord_obj = Landlord.objects.get(id=landlord)
        apartments = Apartment.objects.filter(landlord=landlord_obj)
        items = Unit.objects.filter(apartment__in=apartments)
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST or None, user=agent)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No. {house_name}  added successfully')
                return redirect('dashboard-rental-landlord')
        else:
            add_unit_form = unitForm()
        
        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/rental_landlord.html', context)

@login_required(login_url='user-login')
def assign_unit(request):
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        apartments = Apartment.objects.filter(landlord=landlord)
        items = Unit.objects.filter(apartment__in=apartments)
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No.{house_name}  added successfully')
                return redirect('dashboard-assign-unit')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/assign_unit.html', context)
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        apartments = Apartment.objects.filter(agent=agent)
        items = Unit.objects.filter(apartment__in=apartments)
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No.{house_name} added successfully')
                return redirect('dashboard-assign-unit')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/assign_unit.html', context)
    else:
        items = Unit.objects.all()
        if request.method == 'POST':
            add_unit_form = unitForm(request.POST)
            if add_unit_form.is_valid():
                add_unit_form.save()
                house_name = add_unit_form.cleaned_data.get('door_no')
                messages.success(request, f'House No.{house_name} added successfully')
                return redirect('dashboard-assign-unit')
        else:
            add_unit_form = unitForm()

        context = {
            'items':items,
            'add_unit_form':add_unit_form,
        }
        return render(request, 'dashboard/assign_unit.html', context)


@login_required(login_url='user-login')
def tenant(request):
    if request.user.groups.filter(name='Landlord').exists(): 
        landlord = Landlord.objects.get(name = request.user)
        items = Tenant.objects.filter(landlord=landlord)
        if request.method == 'POST':
            add_tenant_form = TenantcreateForm(request.POST)
            if add_tenant_form.is_valid():
                new_tenant = add_tenant_form.save(commit=False)
                new_tenant.landlord = landlord  # set the landlord field on the new tenant
                new_tenant.save()
                Tenant_name = add_tenant_form.cleaned_data.get('name')
                messages.success(request, f'{Tenant_name} has been added successfully')
                return redirect('dashboard-tenant')
        else:
            add_tenant_form = TenantcreateForm()

        context = {
            'items': items,
            'add_tenant_form':add_tenant_form,
        }

        return render(request, 'user/tenant.html', context)
    elif request.user.groups.filter(name='Agent').exists(): 
        agent = Agent.objects.get(name = request.user)
        landlord = Landlord.objects.filter(agent=agent)
        items = Tenant.objects.filter(landlord__in=landlord)
        if request.method == 'POST':
            add_tenant_form = TenantcreateForm(request.POST)
            if add_tenant_form.is_valid():
                new_tenant = add_tenant_form.save(commit=False)
                
                new_tenant.save()
                return redirect('dashboard-tenant')
        else:
            add_tenant_form = TenantcreateForm()
        context = {
            'items': items,
            'add_tenant_form':add_tenant_form,
        }

        return render(request, 'user/tenant.html', context)
    else:
        items = Tenant.objects.all()
        if request.method == 'POST':
            add_tenant_form = TenantcreateForm(request.POST)
            if add_tenant_form.is_valid():
                new_tenant = add_tenant_form.save(commit=False)
                
                new_tenant.save()
                return redirect('dashboard-tenant')
        else:
            add_tenant_form = TenantcreateForm()
        context = {
            'items': items,
            'add_tenant_form':add_tenant_form,
        }

        return render(request, 'user/tenant.html', context)

@login_required(login_url='user-login')
def tenant_landlord(request, landlord):
        
        landlord = Landlord.objects.filter(id=landlord)
        items = Tenant.objects.filter(landlord__in=landlord)
        if request.method == 'POST':
            add_tenant_form = TenantcreateForm(request.POST)
            if add_tenant_form.is_valid():
                new_tenant = add_tenant_form.save(commit=False)
                new_tenant.landlord = landlord
                new_tenant.save()
                return redirect('dashboard-tenant-landlord')
        else:
            add_tenant_form = TenantcreateForm()
        context = {
            'items': items,
            'add_tenant_form':add_tenant_form,
        }

        return render(request, 'dashboard/tenant_landlord.html', context)

@login_required(login_url='user-login')
def landlord_detail(request):
    agent = Agent.objects.get(name = request.user)
    landlords = Landlord.objects.filter(agent=agent) 

    landlord_data = []  
    for ld in landlords:
                landlord1 = Landlord.objects.get(name = ld.name)
                apts = Apartment.objects.filter(landlord=landlord1)
                No_Apts = apts.count()
                units = Unit.objects.filter(apartment__in=apts)
                Units_count = units.count()
                tenants = Tenant.objects.filter(landlord=landlord1)
                Tenants_count = tenants.count()
                Expected_Amount = units.aggregate(Sum('rent'))['rent__sum'] or 0
                landlord_data.append({
                    'Landlord':landlord1,
                    'apartment_count':No_Apts,
                    'unit_count':Units_count,
                    'Tenants_count': Tenants_count,
                    'Expected_Amount': Expected_Amount,
                    })
                
    context ={
        'landlord_data':landlord_data,
    }
                
    return render(request, 'dashboard/landlord_detail.html', context)

@login_required(login_url='user-login')
def landlord_delete(request, landlord):
    item = Landlord.objects.get(id=landlord)

    if request.method=='POST':
        item.agent = None
        item.save()

        return redirect('dashboard-landlord-detail')
    
    context = {
        'item': item
    }
    return render(request, 'dashboard/landlord_delete.html', context)

