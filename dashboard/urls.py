from django.urls import path
from . import views, reports

urlpatterns = [
    path('receipt/excel/', reports.receipt_excel, name='receipt-excel'),
    path('landlord/receipt/', reports.landlord_receipt, name='landlord-receipt'),
    path('monthly/receipt/', reports.monthly_receipt, name='monthly-receipt'),
    path('tenant/arrear/', reports.tenant_arrear, name='tenant-arrear'),
    path('landlord/units/', reports.landlord_units, name='landlord-units'),

    path('dashboard/', views.index, name='dashboard-index'),
    path('apartment/<int:pk>/', views.apartment, name='dashboard-apartment'),
    path('receipt/', views.receipt, name='dashboard-receipt'),
    path('flat/landlord/<int:landlord>/', views.flat_landlord, name='dashboard-flat-landlord'),
    path('receipt/landlord/<int:landlord>/', views.receipt_landlord, name='dashboard-receipt-landlord'),
    path('rental/landlord/<int:landlord>/', views.rental_landlord, name='dashboard-rental-landlord'),
    path('tenant/landlord/<int:landlord>/', views.tenant_landlord, name='dashboard-tenant-landlord'),
    path('paid/tenant/<int:landlord>/', views.paid_tenant, name='dashboard-paid-tenant'),
    path('tenant/arrears<int:landlord>/', views.tenant_arrears, name='dashboard-tenant-arrears'),
    path('flat/', views.flat, name='dashboard-flat'),
    path('tenant/', views.tenant, name='dashboard-tenant'),
    path('rental/', views.rental, name='dashboard-rental'),
    path('paid/record/', views.paid_record, name='dashboard-paid-record'),
    path('landlord/detail/', views.landlord_detail, name='dashboard-landlord-detail'),
    path('landlord/delete/<int:landlord>/', views.landlord_delete, name='dashboard-landlord-delete'),
    path('unit/payment/<int:pk>/', views.unit_payment, name='dashboard-unit-payment'),
    path('unit/update/<int:pk>/', views.unit_update, name='dashboard-unit-update'),
    path('assign/unit/', views.assign_unit, name='dashboard-assign-unit'),
    path('agent/index/', views.agent_index, name='dashboard-agent-index'),
    path('landlord/index/', views.landlord_index, name='dashboard-landlord-index'),

   

]