from django.urls import path
from item import views

urlpatterns = [
    path('types/', views.ListCreateItemTypes.as_view()),
    path('details/', views.ListCreateItems.as_view()),
    path('update/<int:pk>/', views.UpdateItems.as_view()),
]