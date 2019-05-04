from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from client.models import Client
from client.serializers import ClientSerializer

class SearchClient(APIView):

    def get(self, request, format = None):
        print('data received', request.query_params)
        client_name = request.query_params['clientName']
        queryset = Client.objects.filter(name__icontains = client_name)
        clients = ClientSerializer(queryset, many=True)
        return Response(clients.data)


class ClientView(APIView):

    def get(self, request, id, format = None):
        client = Client.objects.get(pk = id) 
        client_serialized = ClientSerializer(client)
        return Response(client_serialized.data)

    def put(self, request, id, format = None):
        client_existing = Client.objects.get(pk = id)
        serializer = ClientSerializer(client_existing, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateClient(APIView):

    def post(self, request, format = None):
        print("In client create post")
        client_serializer = ClientSerializer(data = request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response(client_serializer.data, status = status.HTTP_201_CREATED)
        return Response(client_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        


