from django.db.models import Count, Sum
from django.views import View
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Bill, BillDescription, PaymentDetails
from client.models import Client
from client.serializers import ClientSerializer
from .serializers import BillSerializer, PaymentDetailsSerializer

import datetime


class CreateBill(APIView):

    def post(self, request, format = None):
        bill = request.data.pop('bill')
        client = request.data.pop('client')
        payment_details = request.data.pop('paymentDetails')
        bill_description = request.data.pop('billDescription')
        company_name = request.data.pop('companyName')
        discount = request.data.pop('discount')

        total_amount = bill['total_amount']*100/(100 - (int(discount))) 

        bill['client'] = client['id']

        bill_serializer = BillSerializer(data=bill)
        if bill_serializer.is_valid():
            bill_serializer.save(payment_details = payment_details,
                                bill_description = bill_description,
                                client_details = client,
                                company_name = company_name,
                                discount = discount,
                                total_amount_w_o_discount = total_amount)
            return Response(bill_serializer.data)
        else:
            return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBillReports(APIView):

   def get(self, request, format = None):
        start_date = datetime.datetime.strptime(request.query_params['startdate'],
                                        '%Y-%m-%dT%H:%M:%S.%fZ').date()
        end_date = datetime.datetime.strptime(request.query_params['enddate'],
                                        '%Y-%m-%dT%H:%M:%S.%fZ').date()

        queryset = []
                                    
        if start_date == end_date:
            queryset = PaymentDetails.objects.filter(date_of_payment = start_date).values('mode_of_payment').annotate(sub_total = Sum('bill__total_amount'), count = Count('mode_of_payment')).order_by('sub_total')

        else:
            queryset = PaymentDetails.objects.filter(date_of_payment__gte = start_date).filter(date_of_payment__lte = end_date).values('mode_of_payment').annotate(sub_total = Sum('bill__total_amount'), count = Count('mode_of_payment')).order_by('sub_total')
         
        bills_report = PaymentDetailsSerializer(queryset, many = True)
        return Response(bills_report.data)

class GetUpdateBill(APIView):

    def get(self, request, id, format = None):
        bill = Bill.objects.get(pk = id)
        bill_serialized = BillSerializer(bill)
        client = Client.objects.get(pk = bill_serialized.data['client'])
        client_serialized = ClientSerializer(client)
        data = {'bill': bill_serialized.data, 'client': client_serialized.data}
        return Response(data)

    def put(self, request, id, format = None):
        bill_existing = Bill.objects.get(pk = id)
        bill_serialized = BillSerializer(bill_existing, data = request.data['bill'])
        if bill_serialized.is_valid():
            bill_serialized.save()
            return Response(data = {'bill': bill_serialized.data})
        return Response(bill_serialized.errors, status = status.HTTP_400_BAD_REQUEST)

class GetBillTemplate(View):

    template_name = 'bill_template.html'

    def get(self, request):

        bill = {'id': 189, 'total_amount': 3500, 'received_amount': 2000, 'balance': 1500, 'rs_in_words':'Three Thousand and Five Hundred'}

        bill_description = [{'description': 'Chin', 'no_of_sessions': '1', 'package_amount': 30}, 
                            {'description': 'Brazilian', 'no_of_sessions': '2', 'package_amount': 950}]
        
        payment_details = {'mode_of_payment': 'Credit Card/NEFT', 'card_no': '124 3254 4565', 
            'approval_code': '13435', 'date_of_payment': '2018-12-02', 'bank_name': 'ICICI', 
            'booking_done_name': 'John Doe'}


        client = {'name': 'Frodo', 'address': 'Shire', 
                'mobile_no': '1234567899', 'email_id': 'sg@gmail.com'}

        data = {'bill': bill, 'bill_description': bill_description,
                'client': client, 'payment_details': payment_details}

        return render(request, self.template_name, {'data': data})        

