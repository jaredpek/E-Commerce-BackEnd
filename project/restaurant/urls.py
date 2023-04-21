from django.urls import path
from restaurant import views

urlpatterns = [
    path('details/', views.ListCreateRestaurants.as_view()),
    path('update/<int:pk>/', views.UpdateRestaurants.as_view()),
]