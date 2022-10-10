from django.urls import path
from . import views

urlpatterns = [
    path('centres_list', views.centre_list_view),
    path('centres_form', views.centre_form_view),
]

