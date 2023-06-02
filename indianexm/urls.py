from django.urls import path
from . import views

urlpatterns = [
    #Home view for EARs
    path('home', views.indianexm_home_view, name='indianexm_home'),

    #upload file screen
    path('indianexm_upload', views.indianexm_upload_view, name='indianexm_upload'),
    path('indianexm_single_file_upload', views.indianexm_single_file_upload_view, name='indianexm_single_file_upload'),


]

