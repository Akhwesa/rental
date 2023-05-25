from django import forms
from .models import Unit, Feed, Apartment

class unitForm(forms.ModelForm):
    

    def __init__(self,  *args, **kwargs ):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter the available apartments based on the current user's related landlord objects.
            self.fields['apartment'].queryset = Apartment.objects.filter(landlord=user)

    class Meta:
        model = Unit
        fields = ['type', 'door_no', 'apartment', 'rent']
        labels = {'rent':'Rent Per Month',}

        
class unitUpdateForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'


class apartmentForm(forms.ModelForm):
   
    class Meta:
        model = Apartment
        fields = ['name', 'apt_no', 'location' ]
        labels = {'name':'name', 'apt_no':'Plot No.'}

class agentapartmentForm(forms.ModelForm):
   
    class Meta:
        model = Apartment
        fields = ['name', 'apt_no', 'location', 'landlord' ]
        labels = {'name':'name', 'apt_no':'Plot No.'}


