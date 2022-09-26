import json
import jwt
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Customer

# Create your tests here.
class TestAPI(TestCase):
    def test_register(self):
        client = APIClient()
        testUser = {
            "id": 123456,
            "firstName": "test",
            "lastName": "user",
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/new', testUser, format='json')
        #print(response)
        #print(dir(response))
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Cliente agregado")

    def test_login(self):
        client = APIClient()
        testUser = Customer(
            id = 123456,
            firstName = "test",
            lastName = "user",
            email = "test@user.com",
            password = "12345"
        )
        testUser.save()

        testLoginData = {
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/login', testLoginData, format='json')
        tokenData = json.loads(response.content)
        #print(response)
        #print(dir(response))
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in tokenData.keys())
        self.assertTrue('refresh' in tokenData.keys())
        self.assertTrue('id' in tokenData.keys())

    def test_getCustomer(self):
        client = APIClient()
        testUser = Customer(
            id = 123456,
            firstName = "test",
            lastName = "user",
            email = "test@user.com",
            password = "12345"
        )
        testUser.save()

        testLoginData = {
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/login', testLoginData, format='json')
        tokenData = json.loads(response.content)
        accessToken = tokenData['access']
        id = tokenData['id']
        url = '/read/' + str(id)
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + accessToken}
        
        response = client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        userData = json.loads(response.content)
        self.assertEqual(userData['email'], "test@user.com")
        self.assertEqual(userData['firstName'], "test")

