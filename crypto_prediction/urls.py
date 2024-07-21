# crypto_prediction/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_crypto_price, name='predict_crypto_price'),
]
