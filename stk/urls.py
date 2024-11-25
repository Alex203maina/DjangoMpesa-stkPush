from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='home'),
    path('payment/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
]