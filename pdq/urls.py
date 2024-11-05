from django.urls import path
from . import views

urlpatterns = [
    #Home view for PDQs
    path('', views.pdq_home, name='pdq_home'),

]
