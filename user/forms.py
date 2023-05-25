from django import forms
from .models import Tenant, Landlord, Agent
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    email = forms.EmailField
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class TenantcreateForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [ 'name','phone', 'te_id', 'mail', 'landlord']
        labels = {'te_id':'National ID'}

class TenantUpdateForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [ 'name','phone', 'te_id', 'mail']
        labels = {'te_id':'National ID'}

class LandlordUpdateForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = [ 'phone', 'ld_id', 'gender']
        labels = {'ld_id':'National ID', 'gender':'Prefix',}

class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [ 'phone', 'agt_id', 'gender']
        labels = {'agt_id':'National ID', 'gender':'Prefix',}
