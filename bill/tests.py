from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Bill, BillDescription, PaymentDetails
from client.models import Client

# Create your tests here.

class BillTest(APITestCase):

    bill_create_url = reverse('create-bill')
    reports_url = reverse('get-reports')
    #get_update_bill_url = reverse('get-update-bill')

    api_client = APIClient()

    def setUp(self):
        user = User.objects.create_user(username='EleganceTestUser', email='elegance@gmail.com', password='Glass_Onion')
        token = Token.objects.create(user=user)

        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.client_1 = Client.objects.create(name= 'Leo Tolstoy', address= 'Dummy Address', 
        mobile_no= '123456789', email_id= 'dummy@gmail.com')

        self.client_2 = Client.objects.create(name= 'Leon', address= 'Dummy Address', 
                mobile_no= '123456789', email_id= 'dummy@gmail.com')

        self.client_3 = Client.objects.create(name= 'Frodo', address= 'Dummy Address', 
                mobile_no= '123456789', email_id= 'sg@gmail.com')

        self.bill_1 = Bill.objects.create(total_amount = 3500, received_amount = 2000, balance= 1500, 
                    rs_in_words='Three Thousand and Five Hundred', client= self.client_1)


    def test_post_bill_valid(self):
        bill_valid = {'total_amount': 3500, 'received_amount': 2000, 'balance': 1500, 
                    'rs_in_words':'Three Thousand and Five Hundred'}

        bill_description_valid = [{'description': 'Chin', 'no_of_sessions': '1', 'package_amount': 30}, 
                            {'description': 'Brazilian', 'no_of_sessions': '2', 'package_amount': 950}]
        
        payment_details = {'mode_of_payment': 'Credit Card/NEFT', 'card_no': '124 3254 4565', 
            'approval_code': '13435', 'date_of_payment': '2018-12-02', 'bank_name': 'ICICI', 
            'booking_done_name': 'John Doe'}


        client = {'id': self.client_3.pk, 'name': 'Frodo', 'address': 'Shire', 
                'mobile_no': '1234567899', 'email_id': 'sg@gmail.com'}

        data = {'bill': bill_valid, 'billDescription': bill_description_valid,
                'client': client, 'paymentDetails': payment_details,
                'companyName': 'Elegance Wellness', 'discount': '10'}


        response = self.api_client.post(self.bill_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_bill_total_amount_invalid(self):
    #     bill = {'received_amount': 2000, 'balance': 1500, 
    #                 'rs_in_words':'Three Thousand and Five Hundred'}

    #     bill_description = [{'description': 'Chin', 'no_of_sessions': '1', 'package_amount': 30}, 
    #                         {'description': 'Brazilian', 'no_of_sessions': '2', 'package_amount': 950}]
        
    #     payment_details = {'mode_of_payment': 'Credit Card/NEFT', 'card_no': '124 3254 4565', 
    #         'approval_code': '13435', 'date_of_payment': '2018-12-02', 'bank_name': 'ICICI', 
    #         'booking_done_name': 'John Doe'}


    #     client = {'id': self.client_2.pk, 'name': 'Frodo', 'address': 'Shire', 
    #             'mobile_no': '1234567899', 'email_id': 'sg@gmail.com'}

    #     data = {'bill': bill, 'billDescription': bill_description,
    #             'client': client, 'paymentDetails': payment_details,
    #             'companyName': 'Elegance Wellness', 'discount': '10'}


    #     response = self.api_client.post(self.bill_create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_bill_no_of_sessions(self):
        bill = {'total_amount': 3500,'received_amount': 2000, 'balance': 1500, 
                    'rs_in_words':'Three Thousand and Five Hundred'}

        bill_description = [{'description': 'Chin', 'package_amount': 30}, 
                            {'description': 'Brazilian', 'package_amount': 950}]
        
        payment_details = {'mode_of_payment': 'Credit Card/NEFT', 'card_no': '124 3254 4565', 
            'approval_code': '13435', 'date_of_payment': '2018-12-02', 'bank_name': 'ICICI', 
            'booking_done_name': 'John Doe'}


        client = {'id': self.client_2.pk, 'name': 'Frodo', 'address': 'Shire', 
                'mobile_no': '1234567899', 'email_id': 'sg@gmail.com'}

        data = {'bill': bill, 'billDescription': bill_description,
                'client': client, 'paymentDetails': payment_details,
                'companyName': 'Elegance Wellness', 'discount': '10'}


        response = self.api_client.post(self.bill_create_url, data, format='json')
        print('Response of post',response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bill(self):
        response = self.api_client.get(reverse('get-update-bill', kwargs= {'id': self.bill_1.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_bill_valid(self):

        bill = {'id': self.bill_1.pk,'total_amount': 3500, 'received_amount': 2000, 'balance': 1500, 
                    'rs_in_words':'Three Thousand and Five Hundred'}

        data = {'bill': bill}

        response_put = self.api_client.put(reverse('get-update-bill', kwargs= {'id': self.bill_1.pk}), data)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
