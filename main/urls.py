from django.urls import path
from . import views
from .views import ping

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('ping/', ping),
]
