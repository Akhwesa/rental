from django.db import models
from django.contrib.auth.models import User

# Create your models here.
gender =(
    ('Mr', 'Mr'), 
    ('Mrs', 'Mrs'),)


class Agent(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    agt_id = models.IntegerField(unique=True)
    gender = models.CharField(max_length=50, choices=gender)
    phone = models.IntegerField()
    mail = models.EmailField()

    def __str__(self):
        return f'{self.name} - Agent'
    
class Landlord(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True )
    ld_id = models.IntegerField(unique=True)
    gender = models.CharField(max_length=50, choices=gender)
    phone = models.IntegerField()
    mail = models.EmailField()
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    te_id = models.IntegerField(unique=True)
    phone = models.IntegerField()
    mail = models.EmailField()
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True,  related_name='Landlords')


    def __str__(self):
        return f'{self.name}'