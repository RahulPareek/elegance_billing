from rest_framework import serializers

from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'mobile_no', 'email_id')