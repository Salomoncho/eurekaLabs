from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('stock-service/', views.StockServiceAPIView.as_view(), name='stock-service'),
]
