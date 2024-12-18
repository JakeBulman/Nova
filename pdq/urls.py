from django.urls import path
from . import views

urlpatterns = [
    #Home view for PDQs
    path('', views.pdq_home, name='pdq_home'),

    #sessions
    path('session_control', views.session_control, name='session_control'),
    path('add_session', views.add_session, name='add_session'),
    path('add_session_complete', views.add_session_complete, name='add_session_complete'),
    path('change_session/<str:session_id>', views.change_session, name='change_session'),
    path('remove_session/<int:session_id>', views.remove_session, name='remove_session'),

    #entries
    path('script_requests', views.script_requests, name='script_requests'),
    path('pdqcsv_create', views.pdqcsv_create, name='pdqcsv_create'),
    path('pdqcsv_download/<str:download_id>', views.pdqcsv_download, name='pdqcsv_download'),
    path('held_scripts', views.held_scripts, name='held_scripts'),

]
