from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
