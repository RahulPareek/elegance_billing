from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from rest_framework import serializers

from .models import Bill, BillDescription, PaymentDetails


class BillDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillDescription
        fields = ('description', 'no_of_sessions', 'package_amount')


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        #depth = 1
        fields = ('id', 'total_amount', 'received_amount', 'balance', 'rs_in_words', 
        'client')

    def create(self, *validated_data):
        payment_details = validated_data[0].pop('payment_details')
        bill_descriptions = validated_data[0].pop('bill_description')
        company_name = validated_data[0].pop('company_name')
        discount = validated_data[0].pop('discount')
        client = validated_data[0].pop('client_details')
        total_amount_w_o_discount = validated_data[0].pop('total_amount_w_o_discount')

        bill_saved = Bill.objects.create(**validated_data[0])
        payment_details_saved = PaymentDetails.objects.create(bill = bill_saved, **payment_details)
        for bill_description in bill_descriptions:
            BillDescription.objects.create(bill = bill_saved, **bill_description)
        
        if client['email_id']:
            subject = 'Elegance Bill: ' + str(bill_saved.id)
            from_id = 'elegancewellness.billing@gmail.com'
            to = client['email_id']

            data = {'client': client, 'bill_descriptions': bill_descriptions,
                            'bill': bill_saved, 'payment_details': payment_details, 
                            'company_name': company_name,
                            'discount': discount,
                            'total_amount_w_o_discount': total_amount_w_o_discount}

            mail_content = render_to_string('bill_template.html', {'data': data})
            text_content = strip_tags(mail_content)

            message = EmailMultiAlternatives(subject, text_content, from_id, [to,])
            message.attach_alternative(mail_content, "text/html")
            message.content_subtype = "html"
            message.send()

        return bill_saved


class PaymentDetailsSerializer(serializers.Serializer):
    mode_of_payment = serializers.CharField(max_length = 100)
    count = serializers.IntegerField()
    sub_total = serializers.DecimalField(max_digits= 20, decimal_places= 4)