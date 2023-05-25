from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  UserUpateForm, TenantUpdateForm, LandlordUpdateForm, AgentUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Tenant, Landlord, Agent, User
from dashboard.models import Apartment
from django.contrib.auth.decorators import login_required

# Create your views here.

def tenant_update(request, pk):

    item = Tenant.objects.get(id=pk)
    
    if request.method == 'POST':
        form = TenantUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            tenant_name = form.cleaned_data.get('name')
            messages.success(request, f'{tenant_name} Updated successfully')
            return redirect('user-tenant-update', pk = pk)
    else:
        form = TenantUpdateForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'user/tenant_update.html', context)

def tenant_delete(request, pk):
    item = Tenant.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-tenant')
    
    context = {
        'item': item
    }
    return render(request, 'user/tenant_delete.html', context)

def agent_delete(request, pk):
    item = Agent.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('user-agent')
    
    context = {
        'item': item
    }
    return render(request, 'user/agent_delete.html', context)

def profile(request):
    return render(request, 'user/profile.html')

def agent(request):
    
    landlord = Landlord.objects.get(name =  request.user)
    agent = landlord.agent
    context = {
        'agent':agent
    }
    return render(request, 'user/agent.html', context)

def landlord_update(request):
    if request.method =='POST':
        user_form = UserUpateForm(request.POST, instance=request.user)
        landlord_form = LandlordUpdateForm(request.POST, request.FILES, instance=request.user.landlord)
        if user_form.is_valid() and landlord_form.is_valid():
            user_form.save()
            landlord_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpateForm(instance=request.user)
        landlord_form = LandlordUpdateForm(instance=request.user.landlord)

    context = {
        'user_form':user_form,
        'landlord_form':landlord_form,
    }
    return render(request, 'user/landlord_update.html', context)

def agent_update(request):
    if request.method =='POST':
        user_form = UserUpateForm(request.POST, instance=request.user)
        agent_form = AgentUpdateForm(request.POST, request.FILES, instance=request.user.agent)
        if user_form.is_valid() and agent_form.is_valid():
            user_form.save()
            agent_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpateForm(instance=request.user)
        agent_form = AgentUpdateForm(instance=request.user.agent)

    context = {
        'user_form':user_form,
        'agent_form':agent_form,
    }
    return render(request, 'user/agent_update.html', context)

def change_password(request, pk):
    item = User.objects.get(id = pk)

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=item)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = PasswordChangeForm(user=item)
    context = {
        'form': form,
    }
    return render(request, 'user/change_password.html', context)