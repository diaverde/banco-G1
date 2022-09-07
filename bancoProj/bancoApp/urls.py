from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('new', views.newCustomer, name='newCustomer'),
    path('read', views.getAllCustomers, name='getAllCustomers'),
    path('read/<int:id>', views.getOneCustomer, name='getOneCustomer'),
]