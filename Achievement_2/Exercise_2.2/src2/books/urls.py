from django.urls import path
from sales.views import home

urlpatterns = [
    path('', home, name='home'),
]

