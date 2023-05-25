from django.contrib import admin
from .models import Apartment, Unit, Payment,Feed, status

# Register your models here.
admin.site.register(Apartment)
admin.site.register(Unit)
admin.site.register(Payment)
admin.site.register(Feed)
admin.site.register(status)
