from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('search/', views.SearchClient.as_view(), name='search-client'),
    path('<int:id>/', views.ClientView.as_view(), name='client'),
    path('create/', views.CreateClient.as_view(), name = 'create-client'),
]