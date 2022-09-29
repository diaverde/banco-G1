from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path('home', views.home, name='home'),
    #path('login', views.login, name='login'),
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('new', views.newCustomer, name='newCustomer'),
    path('read', views.getAllCustomers, name='getAllCustomers'),
    path('read/<int:id>', views.getOneCustomer, name='getOneCustomer'),
    #path('read/<int:id>', views.getOneCustomerNoToken, name='getOneCustomer'),
    path('read/<int:id>', views.getOneCustomer, name='getOneCustomer'),
    #path('read/<int:id>', views.getOneCustomerNoToken, name='getOneCustomer'),
    path('delete/<int:id>', views.deleteCustomer, name='deleteCustomer'),
    path('account/new', views.newAccount, name='newAccount'),
    path('account/update/<int:id>', views.updateAccount, name='updateAccount'),
    path('account/delete/<int:id>', views.deleteAccount, name='deleteAccount'),
]