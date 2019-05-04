from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Client

# Create your tests here.
class ClientTest(APITestCase):

    client_search_url = reverse('search-client')
    client_create_url = reverse('create-client')
    
    api_client = APIClient()
    
    def setUp(self):

        user = User.objects.create_user(username='EleganceTestUser', email='elegance@gmail.com', password='Glass_Onion')
        token = Token.objects.create(user=user)

        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.client_1 = Client.objects.create(name= 'Leo Tolstoy', address= 'Dummy Address', 
        mobile_no= '123456789', email_id= 'dummy@gmail.com')
        
        self.client_2 = Client.objects.create(name= 'Leon', address= 'Dummy Address', mobile_no= '123456789', email_id= 'dummy@gmail.com')

        self.client_3 = Client.objects.create(name= 'Fyodor', address= 'Dummy Address', 
        mobile_no= '123456789', email_id= 'dummy@gmail.com')

    def test_search_client(self):
        valid_data = {'name': 'Dummy name', 'address': 'Dummy Address', 
        'mobile_no': '123456789', 'email_id': 'dummy@gmail.com'}

        response = self.api_client.get(self.client_search_url, {'clientName': 'leo'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_client_return_no_result(self):
        response = self.api_client.get(self.client_search_url, {'clientName': 'premchand'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_client_by_id(self):
        response = self.api_client.get(reverse('client', kwargs= {'id': self.client_3.pk}), format='json')
        self.assertEqual(response.data, {'id': self.client_3.pk, 'name': 'Fyodor', 'address': 'Dummy Address', 'mobile_no': '123456789', 'email_id': 'dummy@gmail.com'})

    def test_put_client_by_id(self):
        response_put = self.api_client.put(reverse('client', kwargs= {'id': self.client_3.pk}), {'name': 'Fyodor', 'address': 'Dummy Address', 'mobile_no': '0987654321', 'email_id': 'dummy@gmail.com'})
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        response = self.api_client.get(reverse('client', kwargs={'id' : self.client_3.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_client_valid(self):
        valid_data = {'name': 'Dummy name', 'address': 'Dummy Address', 
                    'mobile_no': '123456789', 'email_id': 'dummy@gmail.com'}

        response = self.api_client.post(self.client_create_url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_client_invalid_name(self):
        data = {'address': 'Dummy Address', 
                    'mobile_no': '123456789', 'email_id': 'dummy@gmail.com'}

        response = self.api_client.post(self.client_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_client_invalid_address(self):
        data = {'name': 'Dummy name', 'mobile_no': '123456789', 'email_id': 'dummy@gmail.com'}

        response = self.api_client.post(self.client_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)