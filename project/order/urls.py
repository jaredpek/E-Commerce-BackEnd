from django.urls import path
from order import views

urlpatterns = [
    path('details/', views.OrderDetails.as_view()),
    path('details/update/<int:pk>/', views.UpdateOrderDetails.as_view()),
    path('items/', views.OrderItemDetails.as_view()),
    path('items/update/<int:pk>/', views.UpdateOrderItemDetails.as_view()),
]