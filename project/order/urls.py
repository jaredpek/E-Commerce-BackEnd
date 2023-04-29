from django.urls import path
from order import views

urlpatterns = [
    path('details/', views.ListCreateOrder.as_view()),
    path('details/update/<int:pk>/', views.UpdateDestroyOrder.as_view()),
]