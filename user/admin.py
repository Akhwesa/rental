from django.contrib import admin
from .models import Tenant, Landlord, Agent

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Landlord)
admin.site.register(Agent)