import email
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError

from .models import Customer, Account

def home(request):
    return HttpResponse("Bienvenida a su banco")

def newCustomer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer = Customer(
                id = data["id"],
                firstName = data["firstName"],
                lastName = data["lastName"],
                email = data["email"],
                password = data["password"]
            )
            customer.save()
            return HttpResponse("Cliente agregado")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['POST'], "Método inválido")

def getAllCustomers(request):
    if request.method == 'GET':
        try:
            customers = Customer.objects.all()
            allCustData = []
            for cust in customers:
                data = {"id": cust.id, "firstName": cust.firstName, "lastName": cust.lastName, "email": cust.email}
                allCustData.append(data)
            resp = HttpResponse()
            resp.headers['Content-Type'] = "text/json"
            resp.content = json.dumps(allCustData)
            return resp
        except:
            return HttpResponseServerError("Error de servidor")
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")

def getOneCustomer(request, id):
    if request.method == 'GET':
        try:
            cust = Customer.objects.filter(id = id).first()
            #print(customer)
            data = {"id": cust.id, "firstName": cust.firstName, "lastName": cust.lastName, "email": cust.email}
            resp = HttpResponse()
            resp.headers['Content-Type'] = "text/json"
            resp.content = json.dumps(data)
            return resp
        except:
            return HttpResponseServerError("Error de servidor")
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")