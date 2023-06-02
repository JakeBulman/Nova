from django.urls import path
from . import views

urlpatterns = [
    #Home view for EARs
    path('home', views.indianexm_home_view, name='indianexm_home'),

]

