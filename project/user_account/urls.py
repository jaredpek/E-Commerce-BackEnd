from django.urls import path, include
from user_account import views

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('details/', views.AccountDetails.as_view())
]