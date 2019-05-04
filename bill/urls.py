from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBill.as_view(), name="create-bill"),
    path('report/', views.GetBillReports.as_view(), name="get-reports"),
    path('<int:id>/', views.GetUpdateBill.as_view(), name = "get-update-bill"),
    path('bill_template/', views.GetBillTemplate.as_view()),
]