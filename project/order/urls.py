from django.urls import path
from order import views

urlpatterns = [
    path('details/', views.OrderDetails.as_view()),
    path('items/', views.OrderItemDetails.as_view()),
]