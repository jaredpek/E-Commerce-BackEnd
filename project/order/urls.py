from django.urls import path
from order import views

urlpatterns = [
    path('details/', views.ListCreateOrder.as_view()),
    path('details/update/', views.UpdateOrder.as_view()),
    path('details/destroy/<int:pk>/', views.DestroyOrder.as_view()),
    path('items/', views.ManageOrderItems.as_view()),
    path('transactions/', views.ListTransactions.as_view()),
]