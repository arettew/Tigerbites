from django.urls import path 

from . import views 

urlpatterns = [
    path('today/', views.today, name='today'),
    path('all/', views.all, name='all')
]