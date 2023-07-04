from django.urls import path
from . import views

urlpatterns = [
    #Home view for EARs
    path('home', views.ear_home_view, name='enquiries_home'),

    #Server reset hidden options
    path('server_options', views.server_options_view, name='server_options'),
    path('server_settings', views.server_settings_view, name='server_settings'),
    path('server_settings_update', views.server_settings_update_view, name='server_settings_update'),
    path('server_short_reset', views.server_short_reset_view, name='server_short_reset'),
    # path('server_long_reset', views.server_long_reset_view, name='server_long_reset'), 
    

    ### Task Manager Control ###

    #Shows all tasks sets to the user
    path('task_manager/my_tasks', views.my_tasks_view, name='my_tasks'),
    path('task_manager/task_router', views.task_router_view, name='task-router'),
    path('task_manager/new_task', views.new_task_view, name='new-task'),
    path('task_manager/self_assign_task/<str:task_id>', views.self_assign_task_view, name='self-assign-task'),
    path('task_manager/manual_apportionment_task/complete', views.manual_apportionment, name='manual-apportionment-complete'),
    path('task_manager/manual_apportionment_task/<str:task_id>', views.manual_apportionment_task, name='manual-apportionment-task'),
    path('task_manager/setbie_task/<str:task_id>', views.setbie_task, name='setbie-task'),
    path('task_manager/setbie_task/<str:enquiry_id>/bie-complete/', views.complete_bie_view, name="bie-complete"),
    path('task_manager/misvrm_task/complete', views.misvrm_task_complete, name='misvrm-complete'),
    path('task_manager/misvrm_task/<str:task_id>', views.misvrm_task, name='misvrm-task'), 
    path('task_manager/pexmch_task/complete', views.pexmch_task_complete, name='pexmch-complete'),
    path('task_manager/pexmch_task/<str:task_id>', views.pexmch_task, name='pexmch-task'),  
    path('task_manager/botapf_task/complete', views.botapf_task_complete, name='botapf-complete'),
    path('task_manager/botapf_task/<str:task_id>', views.botapf_task, name='botapf-task'),  
    path('task_manager/botmaf_task/complete', views.botmaf_task_complete, name='botmaf-complete'),
    path('task_manager/botmaf_task/<str:task_id>', views.botmaf_task, name='botmaf-task'),  
    path('task_manager/exmsla_task/complete', views.exmsla_task_complete, name='exmsla-complete'),
    path('task_manager/exmsla_task/<str:task_id>', views.exmsla_task, name='exmsla-task'), 
    path('task_manager/negcon_task/complete', views.negcon_task_complete, name='negcon-complete'),
    path('task_manager/negcon_task/<str:task_id>', views.negcon_task, name='negcon-task'), 
    path('task_manager/pdacon_task/complete', views.pdacon_task_complete, name='pdacon-complete'),
    path('task_manager/pdacon_task/<str:task_id>', views.pdacon_task, name='pdacon-task'), 
    path('task_manager/peacon_task/complete', views.peacon_task_complete, name='peacon-complete'),
    path('task_manager/peacon_task/<str:task_id>', views.peacon_task, name='peacon-task'), 
    path('task_manager/pumcon_task/complete', views.pumcon_task_complete, name='pumcon-complete'),
    path('task_manager/pumcon_task/<str:task_id>', views.pumcon_task, name='pumcon-task'), 
    path('task_manager/grdrej_task/complete', views.grdrej_task_complete, name='grdrej-complete'),
    path('task_manager/grdrej_task/<str:task_id>', views.grdrej_task, name='grdrej-task'), 
    path('task_manager/mrkamd_task/complete', views.mrkamd_task_complete, name='mrkamd-complete'),
    path('task_manager/mrkamd_task/<str:task_id>', views.mrkamd_task, name='mrkamd-task'), 
    path('task_manager/grdcon_task/complete', views.grdcon_task_complete, name='grdcon-complete'),
    path('task_manager/grdcon_task/<str:task_id>', views.grdcon_task, name='grdcon-task'), 
    path('task_manager/grdchg_task/complete', views.grdchg_task_complete, name='grdchg-complete'),
    path('task_manager/grdchg_task/<str:task_id>', views.grdchg_task, name='grdchg-task'),  


    ### Task List Control ### 

    #Shows all intial enquiry checks (IEC) that need to be actioned
    path('enquiries_list', views.enquiries_list_view, name='enquiries_list'),
    #Shows all intial enquiry checks (IEC) that need to be actioned
    path('enquiries_setbie_list', views.enquiries_bie_view, name='enquiries_setbie_list'),
    #Manual apportioment main screen
    path('manapp_list', views.manapp_list_view, name='manapp_list'),
    #MIS vs RM main screen
    path('misvrm_list', views.misvrm_list_view, name='misvrm_list'),
    #Previous Exminer Checks main screen
    path('pexmch_list', views.pexmch_list_view, name='pexmch_list'),
    #Download ESMCSV to file location
    path('esmcsv_list', views.esmcsv_list_view, name='esmcsv_list'),
    path('exmsla_create', views.esmcsv_create_view, name='exmsla_create'),
    path('exmsla_download/<str:download_id>', views.esmcsv_download_view, name='exmsla_download'),
    #Control Examiner SAL breaches
    path('exmsla_list', views.exmsla_list_view, name='exmsla_list'),
    #Re-do Examiner SAL breaches
    path('remapp_list', views.remapp_list_view, name='remapp_list'),
    #Release for GRDREL to file location
    path('grdrel_list', views.grdrel_list_view, name='grdrel_list'),
    path('grdrel_create', views.grdrel_create_view, name='grdrel_create'),

    ### Enquiry Detail Control ###

    path('enquiries/enquiries_list/<str:enquiry_id>/iec-pass/', views.iec_pass_view, name="iec-pass"),
    path('enquiries/enquiries_list/iec-pass-all/', views.iec_pass_all_view, name="iec-pass-all"),
    path('enquiries/enquiries_list/<str:enquiry_id>/iec-fail/', views.iec_fail_view, name="iec-fail"),
    path('enquiries/enquiries_list/<str:enquiry_id>/pause-enquiry/', views.pause_enquiry, name="pause-enquiry"),
    path('enquiries/enquiries_list/<str:enquiry_id>/prioritise-enquiry/', views.prioritise_enquiry, name="prioritise-enquiry"),
    path('enquiries_detail', views.enquiries_detail, name='enquiries_detail'),
    #Show detailed view for a specific passed enquiry
    path('enquiries_detail/<str:enquiry_id>/', views.enquiries_detail, name='enquiries_detail'),
    #Used as a post destination for searching enquirie
    path('enquiries_detail_search', views.enquiries_detail_search, name='enquiries_detail_search'),


    ### RPA Control ###

    #RPA apportionment views
    path('rpa_apportionment', views.enquiries_rpa_apportion_view, name='rpa_apportionment'),
    path('rpa_apportionment_failure', views.enquiries_rpa_apportion_failure_view, name='rpa_apportionment_failure'),
    path('rpa_apportionment/<str:script_id>/rpa-pass/', views.rpa_apportion_pass_view, name="rpa_apportion_pass"),
    path('rpa_apportionment/<str:script_id>/rpa-fail/', views.rpa_apportion_fail_view, name="rpa_apportion_fail"),
    #RPA marks keying views
    path('rpa_marks_keying', views.enquiries_rpa_marks_keying_view, name='rpa_marks_keying'),
    path('rpa_marks_keying_failure', views.enquiries_rpa_marks_keying_failure_view, name='rpa_marks_keying_failure'),
    path('rpa_marks_keying/<str:script_id>/rpa-pass/', views.rpa_marks_keying_pass_view, name="rpa_marks_keying_pass"),
    path('rpa_marks_keying/<str:script_id>/rpa-fail/', views.rpa_marks_keying_fail_view, name="rpa_marks_keying_fail"),


    ### Examiner Control ###

    #Shows list of all assigned examiners for this series
    path('examiner_list', views.examiner_list_view, name='examiner_list'),
    #Show detailed view for a specific passed examiner
    path('examiner_detail/<str:per_sid>/', views.examiner_detail, name='examiner_detail'),
    #Examiner availability endpoints
    path('examiner_availability/<str:per_sid>/edit', views.examiner_availability_edit_view, name='exm-avail-edit'),
    path('examiner_availability/<str:note_id>/delete', views.examiner_availability_delete, name='exm-avail-delete'),
    path('examiner_availability/<str:per_sid>/', views.examiner_availability_view, name='examiner_availability'),
    #Examiner notes endpoints
    path('examiner_notes/<str:per_sid>/edit', views.examiner_notes_edit_view, name='exm-notes-edit'),
    path('examiner_notes/<str:note_id>/delete', views.examiner_notes_delete, name='exm-notes-delete'),
    path('examiner_notes/<str:per_sid>/', views.examiner_notes_view, name='examiner_notes'),
    #Examiner conflicts endpoints
    path('examiner_conflicts/<str:per_sid>/edit', views.examiner_conflicts_edit_view, name='exm-conflicts-edit'),
    path('examiner_conflicts/<str:per_sid>/', views.examiner_conflicts_view, name='examiner_conflicts'),
    path('examiner_conflicts/<str:note_id>/delete', views.examiner_conflicts_delete, name='exm-conflicts-delete'),
    #Examiner email update endpoints
    path('examiner_email_update/<str:per_sid>/edit', views.examiner_email_edit_view, name='exm-email-edit'),
    path('examiner_email_update/<str:per_sid>/', views.examiner_email_view, name='examiner_email'),




]

