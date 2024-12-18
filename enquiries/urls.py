from django.urls import path
from . import views

urlpatterns = [
    #Home view for EARs
    path('', views.ear_home_view, name='home'),
    path('home', views.ear_home_view, name='enquiries_home'),
    path('ear_home_view_team_alpha', views.ear_home_view_team_alpha, name='ear_home_view_team_alpha'),
    path('ear_home_view_team_delta', views.ear_home_view_team_delta, name='ear_home_view_team_delta'),
    path('ear_home_view_team_gamma', views.ear_home_view_team_gamma, name='ear_home_view_team_gamma'),
    path('ear_home_view_team_kappa', views.ear_home_view_team_kappa, name='ear_home_view_team_kappa'),
    path('ear_home_view_team_lambda', views.ear_home_view_team_lambda, name='ear_home_view_team_lambda'),
    path('ear_home_view_team_omega', views.ear_home_view_team_omega, name='ear_home_view_team_omega'),
    path('ear_home_view_team_sigma', views.ear_home_view_team_sigma, name='ear_home_view_team_sigma'),

    #Server reset hidden options
    path('server_options', views.server_options_view, name='server_options'),
    path('server_settings', views.server_settings_view, name='server_settings'),
    path('server_settings_update', views.server_settings_update_view, name='server_settings_update'),
    path('server_short_reset', views.server_short_reset_view, name='server_short_reset'),
    # path('server_long_reset', views.server_long_reset_view, name='server_long_reset'), 

    ### Task Manager Control ###

    #Shows all tasks sets to the user
    path('task_manager/my_tasks', views.my_tasks_view, name='my_tasks'),
    path('task_manager/set_backlog', views.set_backlog, name='set_backlog'),
    path('task_manager/task_router/<str:task_id>', views.task_router_view, name='task-router'),
    path('task_manager/new_task', views.new_task_view, name='new-task'),
    path('task_manager/add_new_comment', views.new_task_comment_view, name='add_task_comment'),
    path('task_manager/remove_new_comment', views.remove_task_comment_view, name='remove_task_comment'),
    path('task_manager/task_completion', views.task_completion_view, name='task_completion'),
    path('task_manager/user_list', views.user_list_view, name='user-list'),
    path('user_tasks/<str:userid>/', views.user_tasks_view, name='user_tasks'),
    path('task_manager/self_assign_task/<str:task_id>', views.self_assign_task_view, name='self-assign-task'),
    path('task_manager/assign_task_user/<str:user_id>/<str:task_id>', views.assign_task_user_view, name='assign-task-user'),
    path('task_manager/assign_task_user/<str:user_id>/<str:task_id>/<str:selected_user>', views.assign_task_user_selected_view, name='assign-task-user-selected'),
    path('task_manager/manual_apportionment_task/complete', views.manual_apportionment, name='manual-apportionment-complete'),
    path('task_manager/manual_apportionment_task/<str:task_id>', views.manual_apportionment_task, name='manual-apportionment-task'),
    #path('task_manager/setbie_task/<str:task_id>', views.setbie_task, name='setbie-task'),
    #path('task_manager/setbie_task/<str:enquiry_id>/bie-complete/', views.complete_bie_view, name="bie-complete"),
    path('task_manager/nrmacc_task/complete', views.nrmacc_task_complete, name='nrmacc-complete'),
    path('task_manager/nrmacc_task/<str:task_id>', views.nrmacc_task, name='nrmacc-task'), 
    path('task_manager/nrmscs_task/complete', views.nrmscs_task_complete, name='nrmscs-complete'),
    path('task_manager/nrmscs_task/<str:task_id>', views.nrmscs_task, name='nrmscs-task'), 
    path('task_manager/s3send_task/complete', views.s3send_task_complete, name='s3send-complete'),
    path('task_manager/s3send_task/<str:task_id>', views.s3send_task, name='s3send-task'), 
    path('task_manager/s3conf_task/complete', views.s3conf_task_complete, name='s3conf-complete'),
    path('task_manager/s3conf_task/<str:task_id>', views.s3conf_task, name='s3conf-task'), 
    path('task_manager/manual_mis', views.manual_mis, name='manual-mis'),
    path('task_manager/manual_mis_complete', views.manual_mis_complete, name='manual-mis-complete'),
    path('task_manager/misvrm_task/complete', views.misvrm_task_complete, name='misvrm-complete'),
    path('task_manager/misvrm_task/<str:task_id>', views.misvrm_task, name='misvrm-task'), 
    path('task_manager/misvrf_task/complete', views.misvrf_task_complete, name='misvrf-complete'),
    path('task_manager/misvrf_task/<str:task_id>', views.misvrf_task, name='misvrf-task'), 
    path('task_manager/marche_task/complete', views.marche_task_complete, name='marche-complete'),
    path('task_manager/marche_task/<str:task_id>', views.marche_task, name='marche-task'), 
    path('task_manager/pexmch_task/complete', views.pexmch_task_complete, name='pexmch-complete'),
    path('task_manager/pexmch_task/<str:task_id>', views.pexmch_task, name='pexmch-task'),  
    path('task_manager/locmar_task/complete', views.locmar_task_complete, name='locmar-complete'),
    path('task_manager/locmar_task/<str:task_id>', views.locmar_task, name='locmar-task'), 
    path('task_manager/cleric_task/complete', views.cleric_task_complete, name='cleric-complete'),
    path('task_manager/cleric_task/<str:task_id>', views.cleric_task, name='cleric-task'), 
    path('task_manager/scrche_task/complete', views.scrche_task_complete, name='scrche-complete'),
    path('task_manager/scrche_task/<str:task_id>', views.scrche_task, name='scrche-task'), 
    path('task_manager/scrreq_task/complete', views.scrreq_task_complete, name='scrreq-complete'),
    path('task_manager/scrreq_task/<str:task_id>', views.scrreq_task, name='scrreq-task'), 
    path('task_manager/botapf_task/complete', views.botapf_task_complete, name='botapf-complete'),
    path('task_manager/botapf_task/<str:task_id>', views.botapf_task, name='botapf-task'),  
    path('task_manager/botmaf_task/complete', views.botmaf_task_complete, name='botmaf-complete'),
    path('task_manager/botmaf_task/<str:task_id>', views.botmaf_task, name='botmaf-task'),  
    path('task_manager/exmsla_task/complete', views.exmsla_task_complete, name='exmsla-complete'),
    path('task_manager/exmsla_task/<str:task_id>', views.exmsla_task, name='exmsla-task'), 
    path('task_manager/remapp_task/complete', views.remapp_task_complete, name='remapp-complete'),
    path('task_manager/remapp_task/<str:task_id>', views.remapp_task, name='remapp-task'), 
    path('task_manager/remapf_task/complete', views.remapf_task_complete, name='remapf-complete'),
    path('task_manager/remapf_task/<str:task_id>', views.remapf_task, name='remapf-task'), 
    path('task_manager/negcon_task/complete', views.negcon_task_complete, name='negcon-complete'),
    path('task_manager/negcon_task/<str:task_id>', views.negcon_task, name='negcon-task'), 
    path('task_manager/pdacon_task/complete', views.pdacon_task_complete, name='pdacon-complete'),
    path('task_manager/pdacon_task/<str:task_id>', views.pdacon_task, name='pdacon-task'), 
    path('task_manager/peacon_task/complete', views.peacon_task_complete, name='peacon-complete'),
    path('task_manager/peacon_task/new_scrreq', views.new_scrreq, name='new-scrreq'),
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
    path('task_manager/muprex_task/complete', views.muprex_task_complete, name='muprex-complete'),
    path('task_manager/muprex_task/<str:task_id>', views.muprex_task, name='muprex-task'),

    ### Task List Control ### 

    #Shows all intial enquiry checks (IEC) that need to be actioned
    path('enquiries_list', views.enquiries_list_view, name='enquiries_list'),
    #Shows all intial enquiry checks (IEC) that need to be actioned
    #path('enquiries_setbie_list', views.enquiries_bie_view, name='enquiries_setbie_list'),
    #Manual apportioment main screen
    path('manapp_list', views.manapp_list_view, name='manapp_list'),
    #Non-RM main screen
    path('nrmacc_list', views.nrmacc_list_view, name='nrmacc_list'),
    #Non-RM main screen
    path('nrmscs_list', views.nrmscs_list_view, name='nrmscs_list'),
    #Service 3 main screen
    path('s3send_list', views.s3send_list_view, name='s3send_list'),
    #Service 3 main screen 2
    path('s3conf_list', views.s3conf_list_view, name='s3conf_list'),
    #MIS vs RM main screen
    path('misvrm_list', views.misvrm_list_view, name='misvrm_list'),
    #MIS vs RM recheck main screen
    path('misvrf_list', views.misvrf_list_view, name='misvrf_list'),
    #Mark check main screen
    path('marche_list', views.marche_list_view, name='marche_list'),
    #Previous Exminer Checks main screen
    path('pexmch_list', views.pexmch_list_view, name='pexmch_list'),
    #Locmar Checks main screen
    path('locmar_list', views.locmar_list_view, name='locmar_list'),
    #Clerical Checks main screen
    path('cleric_list', views.cleric_list_view, name='cleric_list'),
    #Script Checks main screen
    path('scrche_list', views.scrche_list_view, name='scrche_list'),
    #Script Re-requests main screen
    path('scrreq_list', views.scrreq_list_view, name='scrreq_list'),
    #Download ESMCSV to file location
    path('esmcsv_list', views.esmcsv_list_view, name='esmcsv_list'),
    path('exmsla_create', views.esmcsv_create_view, name='exmsla_create'),
    path('exmsla_download/<str:download_id>', views.esmcsv_download_view, name='exmsla_download'),
    #Download OMRCHE to file location
    path('omrche_list', views.omrche_list_view, name='omrche_list'),
    path('omrche_create', views.omrche_create_view, name='omrche_create'),
    path('omrche_download/<str:download_id>', views.omrche_download_view, name='omrche_download'),
        #Download OMRSCR to file location
    path('omrscr_list', views.omrscr_list_view, name='omrscr_list'),
    path('omrscr_create', views.omrscr_create_view, name='omrscr_create'),
    path('omrscr_download/<str:download_id>', views.omrscr_download_view, name='omrscr_download'),
    #Download ESMSCR to file location
    path('esmscr_list', views.esmscr_list_view, name='esmscr_list'),
    path('exmscr_create', views.esmscr_create_view, name='exmscr_create'),
    path('exmscr_download/<str:download_id>', views.esmscr_download_view, name='exmscr_download'),
    #Download ESMSC2 to file location
    path('esmsc2_list', views.esmsc2_list_view, name='esmsc2_list'),
    path('exmsc2_create', views.esmsc2_create_view, name='exmsc2_create'),
    path('exmsc2_download/<str:download_id>', views.esmsc2_download_view, name='exmsc2_download'),
    #Script waiting list
    path('scrren_list', views.scrren_list_view, name='scrren_list'),
    path('scrren_sendback', views.scrren_sendback_view, name='scrren_sendback'),
    #Control Examiner SAL breaches
    path('exmsla_list', views.exmsla_list_view, name='exmsla_list'),
    #Re-do Examiner SAL breaches
    path('remapp_list', views.remapp_list_view, name='remapp_list'),
    #Re-do Examiner SAL breaches - EPS Pickup
    path('remapf_list', views.remapf_list_view, name='remapf_list'),
    #Release for GRDREL 
    path('grdrel_create', views.grdrel_create_view, name='grdrel_create'),
    #Previous Exminer Checks main screen
    path('negcon_list', views.negcon_list_view, name='negcon_list'),
    #Previous Exminer Checks main screen
    path('peacon_list', views.peacon_list_view, name='peacon_list'),
    #Previous Exminer Checks main screen
    path('pdacon_list', views.pdacon_list_view, name='pdacon_list'),
    #Grade Changes main screen
    path('grdchg_list', views.grdchg_list_view, name='grdchg_list'),
    #Grade Rejections main screen
    path('grdrej_list', views.grdrej_list_view, name='grdrej_list'),
    #Mark Amendments main screen
    path('mrkamd_list', views.mrkamd_list_view, name='mrkamd_list'),
    #MU examiners main screen
    path('muprex_list', views.muprex_list_view, name='muprex_list'),
    #Release for OUTCON
    path('outcon_create', views.outcon_create_view, name='outcon_create'),

    ### Enquiry Detail Control ###

    path('enquiries/enquiries_list/<str:enquiry_id>/iec-pass/', views.iec_pass_view, name="iec-pass"),
    path('enquiries/enquiries_list/iec-pass-all/', views.iec_pass_all_view, name="iec-pass-all"),
    path('enquiries/enquiries_list/<str:enquiry_id>/iec-fail/', views.iec_fail_view, name="iec-fail"),
    path('enquiries/enquiries_list/<str:enquiry_id>/iec-issue/', views.iec_issue_view, name="iec-issue"),
    path('enquiries/enquiries_list/<str:enquiry_id>/pause-enquiry/', views.pause_enquiry, name="pause-enquiry"),
    path('enquiries/enquiries_list/<str:enquiry_id>/set-issue/', views.set_issue_enquiry, name="set-issue"),
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
    #Show detailed view for a specific passed examiner scripts
    path('examiner_scripts/<str:per_sid>/', views.examiner_scripts_view, name='examiner_scripts'),
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



    #CASE System
    path('case_system', views.case_system_view, name='case_system'),
    path('case_detail/<str:case_id>/', views.case_detail_view, name='case_detail'),
    path('case_system_create', views.create_cases_view, name='case_system_create'),
    path('case_system/self_assign_task/<str:case_id>', views.self_assign_case_view, name='self-assign-case'),
    path('case_system/assign_task_user/<str:user_id>/<str:case_id>', views.assign_case_user_view, name='assign-case-user'),
    path('case_system/assign_task_user/<str:user_id>/<str:case_id>/<str:selected_user>', views.assign_case_user_selected_view, name='assign-case-user-selected'),

    path('case_system/my_cases', views.my_cases_view, name='my_cases'),
    path('case_system/set_backlog_case', views.set_backlog_case, name='set_backlog_case'),
    path('case_system/new_case', views.new_case_view, name='new-case'),
    path('case_system/add_new_comment', views.new_case_comment_view, name='add_case_comment'),
    path('case_system/remove_new_comment', views.remove_case_comment_view, name='remove_case_comment'),


    ### Panel Control ###

    #Shows list of all panels for this series
    path('panel_list', views.panel_list_view, name='panel_list'),
    path('panel_set_manual', views.panel_set_manual_view, name='panel_set_manual'),
    path('panel_update_note', views.panel_update_note_view, name='panel_update_note'),

    ### Admin ###

    #Shows list of all assigned tasks fo users
    path('user_panel', views.user_panel_view, name='user_panel'),
    path('user_remove_tasks', views.user_remove_tasks_view, name='user_remove_tasks'),
    path('create_user', views.create_user_view, name='create_user'),
    path('edit_user/<str:userid>/', views.edit_user_view, name='edit_user'),
    path('update_user', views.update_user_view, name='update_user'),
    path('user_change_secondary', views.user_change_secondary, name='user_change_secondary'),
    path('reload_tolerance', views.reload_tolerance_view, name='reload_tolerance')
]
