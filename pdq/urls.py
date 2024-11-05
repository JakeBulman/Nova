from django.urls import path
from . import views

urlpatterns = [
    #Home view for PDQs
    path('', views.pdq_home, name='pdq_home'),
    path('session_control', views.session_control, name='session_control'),

]
