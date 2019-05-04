from django.contrib import admin
from .models import Bill, BillDescription, PaymentDetails

admin.site.register(Bill)
admin.site.register(BillDescription)
admin.site.register(PaymentDetails)
