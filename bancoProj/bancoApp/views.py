import datetime
import json
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Customer, Account

def home(request):
    return HttpResponse("Bienvenida a su banco")

def newCustomer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cust = Customer.objects.filter(id = data['id']).first()
            if (cust):
                return HttpResponseBadRequest("Ya existe un usuario con ese documento.")

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
            if (not customers):
                return HttpResponseBadRequest("No existen usuarios cargados.")

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
            token = request.META.get('HTTP_AUTHORIZATION')[7:]
            tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = tokenBackend.decode(token, verify=False)
            #print(valid_data)
            if valid_data['user_id'] != id:
                raise Exception
        except:
            return HttpResponse("Credenciales inválidas. Acceso no autorizado.", status=401)

        try:
            #print(request.path)
            cust = Customer.objects.filter(id = id).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            accounts = Account.objects.filter(user = id)
            accountsData = []
            for acc in accounts:
                data = {"number": acc.number, "balance": float(acc.balance)}
                accountsData.append(data)

            #print(customer)
            data = {
                "id": cust.id,
                "firstName": cust.firstName,
                "lastName": cust.lastName,
                "email": cust.email,
                "accounts": accountsData
            }
            resp = HttpResponse()
            resp.headers['Content-Type'] = "text/json"
            resp.content = json.dumps(data)
            return resp
        except:
            return HttpResponseServerError("Error de servidor")
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")

def getOneCustomerNoToken(request, id):
    if request.method == 'GET':
        try:
            #print(request.path)
            cust = Customer.objects.filter(id = id).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            accounts = Account.objects.filter(user = id)
            accountsData = []
            for acc in accounts:
                data = {"number": acc.number, "balance": float(acc.balance)}
                accountsData.append(data)

            #print(customer)
            data = {
                "id": cust.id,
                "firstName": cust.firstName,
                "lastName": cust.lastName,
                "email": cust.email,
                "accounts": accountsData
            }
            resp = HttpResponse()
            resp.headers['Content-Type'] = "text/json"
            resp.content = json.dumps(data)
            return resp
        except:
            return HttpResponseServerError("Error de servidor")
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")

def updateCustomer(request, id):
    if request.method == 'PUT':
        
        try:
            token = request.META.get('HTTP_AUTHORIZATION')[7:]
            tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = tokenBackend.decode(token, verify=False)
            #print(valid_data)
            if valid_data['user_id'] != id:
                raise Exception
        except:
            return HttpResponse("Credenciales inválidas. Acceso no autorizado.", status=401)

        try:
            cust = Customer.objects.filter(id = id).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            data = json.loads(request.body)
            if 'firstName' in data.keys():
                cust.firstName = data["firstName"]
            if 'lastName' in data.keys():
                cust.lastName = data["lastName"]
            if 'email' in data.keys():
                cust.email = data["email"]
            if 'password' in data.keys():
                cust.password = data["password"]
            cust.save()
            return HttpResponse("Cliente actualizado")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['PUT'], "Método inválido")

def updateCustomerNoToken(request, id):
    if request.method == 'PUT':
        
        try:
            cust = Customer.objects.filter(id = id).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            data = json.loads(request.body)
            if 'firstName' in data.keys():
                cust.firstName = data["firstName"]
            if 'lastName' in data.keys():
                cust.lastName = data["lastName"]
            if 'email' in data.keys():
                cust.email = data["email"]
            if 'password' in data.keys():
                cust.password = data["password"]
            cust.save()
            return HttpResponse("Cliente actualizado")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['PUT'], "Método inválido")

def deleteCustomer(request, id):
    if request.method == 'DELETE':
        try:
            cust = Customer.objects.filter(id = id).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            cust.delete()
            return HttpResponse("Cliente eliminado")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['DELETE'], "Método inválido")

# -----------------
# Account
# -----------------

def newAccount(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cust = Customer.objects.filter(id = data["userId"]).first()
            if (not cust):
                return HttpResponseBadRequest("No existe un usuario con ese documento.")

            account = Account(
                lastChangeDate = datetime.datetime.now(),
                user = cust
            )
            account.save()
            return HttpResponse("Cuenta creada")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['POST'], "Método inválido")

def updateAccount(request, id):
    if request.method == 'PUT':
        try:
            account = Account.objects.filter(number = id).first()
            if (not account):
                return HttpResponseBadRequest("No existe esa cuenta.")

            data = json.loads(request.body)
            account.balance = data["balance"]
            account.isActive = data["isActive"]
            account.lastChangeDate = datetime.datetime.now()
            account.save()
            return HttpResponse("Cuenta actualizada")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['PUT'], "Método inválido")

def deleteAccount(request, id):
    if request.method == 'DELETE':
        try:
            account = Account.objects.filter(number = id).first()
            if (not account):
                return HttpResponseBadRequest("No existe esa cuenta.")

            account.delete()
            return HttpResponse("Cuenta eliminada")
        except:
            return HttpResponseBadRequest("Error en los datos recibidos")
    else:
        return HttpResponseNotAllowed(['DELETE'], "Método inválido")

# -----------------
# Login
# -----------------

def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            customer = Customer.objects.filter(email = email, password = password).first()
            if (not customer):
                return HttpResponse("Credenciales inválidas.", status = 401)

            custData = {"id": customer.id}
            resp = HttpResponse()
            resp.headers['Content-Type'] = 'text/json'
            #resp.content = json.dumps(custData)
            token = {
                "access": "eyasfsafsfdsgdgdgdgdhf=",
                "refresh": "eyasfsafsfdsgdgdgdgdhf=",
            }
            resp.content = json.dumps(token)
            return resp
        except:
            return HttpResponseBadRequest("Datos mal enviados")
    else:
        return HttpResponseNotAllowed(["POST"], "Método inválido")

# Nuevas clases heredadas para mejorar token a entregar
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer