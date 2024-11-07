from django.urls import path
from . import views

urlpatterns = [
    #Home view for PDQs
    path('', views.pdq_home, name='pdq_home'),
    path('session_control', views.session_control, name='session_control'),
    path('add_session', views.add_session, name='add_session'),
    path('add_session_complete', views.add_session_complete, name='add_session_complete'),
    path('change_session/<str:session_id>', views.change_session, name='change_session'),
    path('remove_session/<int:session_id>', views.remove_session, name='remove_session'),

]
