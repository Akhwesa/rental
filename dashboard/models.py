from django.db import models
from user.models import Tenant, Landlord, Agent
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
rent_status = (
    ('Paid','Paid'),
    ('In Arrears','In Arrears'),
    ('confirm', 'confirm' ), 
    ('unavailable', 'unavailable'),
    )

unit_status = (
    ('occupied', 'occupied'),
    ('Empty', 'Empty'),
    )

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    apt_no = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    landlord = models.ForeignKey(Landlord,  on_delete=models.SET_NULL, null=True, blank=True, related_name='Landlord')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='Agent')

    def __str__(self):
        return f'{self.name}'

class Unit(models.Model):
    type = models.CharField(max_length=100)
    door_no = models.CharField(max_length=50 )
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartments')
    rent = models.IntegerField()
    tenant = models.OneToOneField(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    Rent_status = models.CharField(max_length=50, choices=rent_status, default='unavailable' )
    hse_status = models.CharField(max_length=50, choices=unit_status, default='Empty' )

    class Meta:
        unique_together = ('door_no', 'apartment')

    def __str__(self):
        return f'{self.door_no} - {self.type}'

class Payment(models.Model):
    accountReference = models.CharField(max_length=50)
    paidAmount = models.DecimalField(max_digits=8, decimal_places=2)
    paymentDate = models.DateField()
    transactionId =  models.CharField(max_length=150)
    phoneNumber = models.IntegerField()
    fullName = models.CharField(max_length=150)
    invoiceName = models.CharField(max_length=150)
    externalReference = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.accountReference}-{self.phoneNumber}-{self.paidAmount} - {self.paymentDate}'
    
class Feed(models.Model):
    feed_update = models.CharField(max_length=250)
    
    def update_feed(self, message):
        self.feed_update = f"{message}"
        self.save()

    def __str__(self):
        return f'{self.feed_update}'
    
class status(models.Model):
        Landlord = models.CharField(max_length=150)
        No_Apartments = models.CharField(max_length=150)
        Units_count = models.CharField(max_length=150)
        Tenants_count = models.CharField(max_length=150)
        Expected_Amount = models.CharField(max_length=150)
        Paid_Tenants= models.CharField(max_length=150)
        Paid_Amount= models.CharField(max_length=150)
        Deficit_Amount= models.CharField(max_length=150)
        Not_Paid_Tenants= models.CharField(max_length=150)

        def __str__(self):
            return f'{self.Landlord}'
