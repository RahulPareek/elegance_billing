from django.db import models
from client.models import Client

class Bill(models.Model):
    total_amount = models.DecimalField(max_digits= 20, decimal_places= 4)
    received_amount = models.DecimalField(max_digits= 20, decimal_places= 4)
    balance = models.DecimalField(max_digits= 20, decimal_places= 4)
    rs_in_words = models.CharField(max_length = 200, null = True, blank = True)
    client = models.ForeignKey(Client, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.client.name + " " + str(self.total_amount)


class BillDescription(models.Model):
    description = models.CharField(max_length = 200)
    no_of_sessions = models.IntegerField(null = True, blank= True, default=1)
    package_amount = models.DecimalField(max_digits= 20, decimal_places= 4)
    bill = models.ForeignKey(Bill, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.description


class PaymentDetails(models.Model):
    mode_of_payment = models.CharField(max_length = 30)
    card_no = models.CharField(max_length = 16, null = True, blank = True)
    date_of_payment = models.DateField()
    approval_code = models.CharField(max_length=100, null = True, blank = True)
    cheque_no = models.CharField(max_length = 100, null = True, blank = True)
    bank_name = models.CharField(max_length = 100, null = True, blank = True)
    booking_done_name = models.CharField(max_length = 100)
    bill = models.ForeignKey(Bill, on_delete = models.CASCADE)

    def __str__(self):
        return self.mode_of_payment


