from django.urls import path
from . import views

urlpatterns = [
    #Home view for datareporting
    path('home', views.datareporting_home_view, name='datareporting_home'),
    path('run_data_load/<int:report_id>', views.run_data_load_view, name='run_data_load'),
    path('update_active_status/<int:report_id>', views.report_update_status, name='update_active_status'),
]
