from django.db import models
from django.contrib.auth.models import User

# Create your models here. DO NOT USE
class Enquiries(models.Model):
    enquiry_id = models.CharField(max_length=10)
    service = models.CharField(max_length=5)
    component_indicator = models.CharField(max_length=1)
    batch = models.CharField(max_length=10, null=True)
    centre_id = models.CharField(max_length=10)
    candidate_number = models.CharField(max_length=10)
    ass_and_vers = models.CharField(max_length=10)
    assessment_name = models.CharField(max_length=50)
    component_id = models.CharField(max_length=4)
    rm_ind = models.CharField(max_length=10)
    submit_date = models.DateTimeField(null=True)
    bie = models.CharField(max_length=10)
    omr_batch = models.CharField(max_length=10,null=True)
    omr_position = models.CharField(max_length=10,null=True)
    completion_date = models.DateTimeField(null=True)
    initial_check_complete = models.BooleanField(default=False)

##########################################################################

class CentreEnquiryRequests(models.Model):
    enquiry_id = models.CharField(max_length=10, unique=True)
    enquiry_status = models.CharField(max_length=1)
    eps_creation_date = models.DateTimeField(null=True)
    eps_completion_date = models.DateTimeField(null=True)
    eps_ack_letter_ind = models.CharField(max_length=1, null=True)
    eps_ses_sid = models.CharField(max_length=5, null=True)
    centre_id = models.CharField(max_length=5, null=True)
    created_by = models.CharField(max_length=50, null=True)
    cie_direct_id = models.CharField(max_length=7, null=True)

class EnquiryRequestParts(models.Model):
    erp_sid = models.CharField(max_length=8, unique=True, default=0)
    cer_sid = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.CASCADE, related_name='enquiries')
    service_code = models.CharField(max_length=5,null=True)
    eps_ses_sid = models.CharField(max_length=5,null=True)
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_ass_ver_no = models.CharField(max_length=2,null=True)
    eps_option_code = models.CharField(max_length=2,null=True)
    eps_cand_unique_id = models.CharField(max_length=20,null=True)
    eps_cand_id = models.CharField(max_length=10,null=True)
    eps_centre_id = models.CharField(max_length=5,null=True)
    eps_comp_ind = models.CharField(max_length=1,null=True)
    eps_script_measure = models.CharField(max_length=8,null=True)
    booked_in_error_ind = models.CharField(max_length=1,null=True)
    stud_name = models.CharField(max_length=100,null=True)

class EnquiryComponents(models.Model):
    ec_sid = models.CharField(max_length=8, unique=True, default=0)
    erp_sid = models.ForeignKey(EnquiryRequestParts, to_field='erp_sid', on_delete=models.CASCADE,  related_name='enquiry_parts')
    eps_ses_sid = models.CharField(max_length=5,null=True)
    eps_ses_name = models.CharField(max_length=30,null=True)
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_ass_ver_no = models.CharField(max_length=2,null=True)
    eps_com_id = models.CharField(max_length=2,null=True)
    eps_qual_id = models.CharField(max_length=5,null=True) #from cie.ca_products
    eps_qual_name = models.CharField(max_length=50,null=True) #from cie.ca_products
    eps_ass_name = models.CharField(max_length=50,null=True) #from cie.ca_products
    eps_comp_name = models.CharField(max_length=50,null=True) #from cie.ca_products
    ccm_measure = models.CharField(max_length=5,null=True)
    script_type = models.CharField(max_length=50,null=True)

class EnquiryComponentsHistory(models.Model):
    cer_sid = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.SET_NULL, related_name='enquiry_original_marks',null=True)
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, related_name='script_original_marks',null=True) 
    eps_ses_sid = models.CharField(max_length=5,null=True)
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_com_id = models.CharField(max_length=2,null=True)
    eps_cnu_id = models.CharField(max_length=5,null=True)
    eps_cand_no = models.CharField(max_length=10,null=True)
    exm_position = models.CharField(max_length=10,null=True)
    kbr_code = models.CharField(max_length=4,null=True)
    kbr_reason = models.CharField(max_length=50,null=True)
    current_mark = models.CharField(max_length=5,null=True)
    ear_mark = models.CharField(max_length=5,null=True)
    ear_mark_alt =models.CharField(max_length=5,null=True)

class EnquiryComponentsExaminerChecks(models.Model):
    cer_sid = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.SET_NULL, related_name='enquiry_pexmch',null=True)
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, related_name='script_pexmch',null=True) 
    eps_ses_sid = models.CharField(max_length=5,null=True)
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_com_id = models.CharField(max_length=2,null=True)
    eps_cnu_id = models.CharField(max_length=5,null=True)
    eps_cand_no = models.CharField(max_length=10,null=True)
    exm_position = models.CharField(max_length=10,null=True)
    kbr_code = models.CharField(max_length=4,null=True)
    kbr_reason = models.CharField(max_length=50,null=True)

class EnquiryComponentsPreviousExaminers(models.Model):
    cer_sid = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.SET_NULL, related_name='enquiry_prev_exm',null=True)
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, related_name='script_prev_exm',null=True) 
    exm_position = models.CharField(max_length=10,null=True)

class TaskTeams(models.Model):
    team_name = models.CharField(max_length=20, unique=True, default='')

class TaskTypes(models.Model):
    task_id = models.CharField(max_length=6, unique=True)
    task_description = models.TextField(null=True)
    task_team = models.ForeignKey(TaskTeams, on_delete=models.SET_NULL, null=True)
    task_rank = models.IntegerField(default=0)

class TaskManager(models.Model):
    enquiry_id = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.SET_NULL, related_name='enquiry_tasks',null=True)
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, related_name='script_tasks',null=True)
    task_id = models.ForeignKey(TaskTypes, to_field='task_id', on_delete=models.SET_NULL, related_name='all_tasks',null=True)
    task_creation_date = models.DateTimeField(auto_now_add=True)
    task_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks',) #Have to use proper user model here instead of strings
    task_assigned_date = models.DateTimeField(null=True) 
    task_completion_date = models.DateTimeField(null=True)   

class TaskUserPrimary(models.Model):
    task_user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_primary')
    primary_team = models.ForeignKey(TaskTeams, on_delete=models.SET_NULL, null=True)
    primary_status = models.CharField(max_length=2, default='')

class TaskUserSecondary(models.Model):
    task_user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    secondary_team = models.ForeignKey(TaskTeams, on_delete=models.SET_NULL, null=True)

class EnquiryBatches(models.Model):   
    eb_sid = models.CharField(max_length=8, unique=True, default=0)
    created_date = models.DateTimeField(null=True)
    enpe_eper_per_sid = models.CharField(max_length=8, null=True)
    
class EnquiryComponentElements(models.Model):
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', related_name='script_id', on_delete=models.CASCADE)
    ece_status = models.CharField(max_length=20, null=True)
    eb_sid = models.ForeignKey(EnquiryBatches, to_field='eb_sid', related_name='batch_id', on_delete=models.SET_NULL, null=True)
    clerical_mark = models.CharField(max_length=5, null=True)
    mark_after_enquiry = models.CharField(max_length=5, null=True)
    justification_code = models.CharField(max_length=5, null=True)

class EnquiryGrades(models.Model):
    enquiry_id = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.SET_NULL, related_name='enquiry_grades',null=True)
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_cand_no = models.CharField(max_length=10,null=True)
    previous_grade = models.CharField(max_length=4,null=True)
    previous_seq = models.CharField(max_length=4,null=True)
    new_grade = models.CharField(max_length=4,null=True)
    new_seq = models.CharField(max_length=4,null=True)

class MarkTolerances(models.Model):
    eps_ass_code = models.CharField(max_length=4,null=True)
    eps_com_id = models.CharField(max_length=2,null=True)
    mark_tolerance = models.CharField(max_length=4,null=True)

class UniqueCreditor(models.Model):
    exm_creditor_no = models.CharField(max_length=8, unique=True, default=0)
    per_sid = models.CharField(max_length=8, unique=True, default=0)
    exm_title = models.CharField(max_length=20, null=True)
    exm_initials = models.CharField(max_length=50, null=True)
    exm_surname = models.CharField(max_length=50, null=True)
    exm_forename = models.CharField(max_length=50, null=True)
    exm_email = models.CharField(max_length=50, null=True)

class EnquiryPersonnel(models.Model):
    enpe_sid = models.CharField(max_length=8, unique=True, default=0)
    sp_sid = models.CharField(max_length=8, null=True)
    per_sid = models.ForeignKey(UniqueCreditor, to_field='per_sid', on_delete=models.CASCADE, null=True, related_name='creditors')

class EnquiryPersonnelDetails(models.Model):
    enpe_sid = models.ForeignKey(EnquiryPersonnel, to_field='enpe_sid', on_delete=models.CASCADE, null=True, related_name='exm_per_details')
    sp_sid = models.CharField(max_length=8, null=True)
    ass_code = models.CharField(max_length=8, null=True)
    com_id = models.CharField(max_length=8, null=True)
    sp_name = models.CharField(max_length=100, null=True)
    sp_ses_sid = models.CharField(max_length=8, null=True)
    sp_use_esm_ind = models.CharField(max_length=8, null=True)
    session = models.CharField(max_length=8, null=True)
    exm_creditor_no = models.CharField(max_length=8, null=True)
    exm_examiner_no = models.CharField(max_length=8, null=True)
    spp_sid = models.CharField(max_length=8, null=True)
    ear_approval_ind = models.CharField(max_length=1, null=True)
    panel_size = models.CharField(max_length=8, null=True)

class ExaminerAvailability(models.Model):
    creditor = models.ManyToManyField(UniqueCreditor, related_name='exm_availability')
    unavailability_start_date = models.DateField(null=True)
    unavailability_end_date = models.DateField(null=True)
    unavailable_2_flag = models.CharField(max_length=1, null=True)
    unavailable_5_flag = models.CharField(max_length=1, null=True)
    unavailable_9_flag = models.CharField(max_length=1, null=True)
    #manual_apportion_ind = models.CharField(max_length=1, null=True) This can't be here or it doesn't work when fully available
    #Syll/Comp, Panel Size, creditor number, examiner name, exm email, exm confict of int, exm notes

class ExaminerNotes(models.Model):
    creditor = models.ManyToManyField(UniqueCreditor, related_name='exm_notes')
    examiner_notes = models.TextField(null=True)
    note_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note_created = models.DateTimeField(auto_now_add=True, null=True)

class ExaminerConflicts(models.Model):
    creditor = models.ManyToManyField(UniqueCreditor, related_name='exm_conflicts')
    examiner_conflicts = models.TextField(null=True)
    note_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note_created = models.DateTimeField(auto_now_add=True, null=True)
    note_modified = models.DateTimeField(auto_now=True, null=True)

class ExaminerEmailOverride(models.Model):
    creditor = models.ManyToManyField(UniqueCreditor, related_name='exm_email_manual')
    examiner_email_manual = models.TextField(null=True)

class ScriptApportionment(models.Model):
    enpe_sid = models.ForeignKey(EnquiryPersonnel, to_field='enpe_sid', on_delete=models.SET_NULL, null=True, related_name='apportion_examiner')
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, null=True, related_name='apportion_script')
    script_marked = models.IntegerField(default=1)
    script_mark_entered = models.IntegerField(default=1)
    apportionment_invalidated = models.IntegerField(default=0)

class ScriptApportionmentExtension(models.Model):
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, null=True, related_name='script_extension')
    task_id = models.ForeignKey(TaskManager, on_delete=models.SET_NULL, null=True, related_name='task_extension')
    extenstion_days = models.CharField(max_length=3, default=0)

class RpaFailureAudit(models.Model):
    rpa_task_key = models.ForeignKey(TaskManager, on_delete=models.CASCADE, null=True, related_name='task_manager_task')
    failure_reason = models.TextField(null=True)

class SetBIEAudit(models.Model):
    rpa_task_key = models.ForeignKey(TaskManager, on_delete=models.CASCADE, null=True, related_name='task_bie_reason')
    failure_reason = models.TextField(null=True)

class GradeFailureAudit(models.Model):
    task_key = models.ForeignKey(TaskManager, on_delete=models.CASCADE, null=True, related_name='task_grade_failure')
    failure_stage = models.ForeignKey(TaskTypes, to_field='task_id', on_delete=models.SET_NULL, null=True)
    failure_reason = models.TextField(null=True)

class SetIssueAudit(models.Model):
    enquiry_id = models.ForeignKey(CentreEnquiryRequests, to_field='enquiry_id', on_delete=models.CASCADE, related_name='enquiry_issues')
    issue_flag = models.IntegerField(default=1)
    issue_reason = models.TextField(null=True)

class MisReturnData(models.Model):
    ec_sid = models.ForeignKey(EnquiryComponents, to_field='ec_sid', on_delete=models.SET_NULL, related_name='script_mis',null=True)
    eb_sid = models.ForeignKey(EnquiryBatches, to_field='eb_sid', on_delete=models.SET_NULL, related_name='batch_mis', null=True)
    original_exm = models.CharField(max_length=10, null=True)
    rev_exm = models.CharField(max_length=10, null=True)
    original_mark = models.CharField(max_length=10, null=True)
    mark_status = models.CharField(max_length=10, null=True)
    revised_mark = models.CharField(max_length=10, null=True)
    justification_code = models.CharField(max_length=20, null=True)
    final_mark = models.CharField(max_length=10, null=True)
    final_justification_code = models.CharField(max_length=10, null=True)
    final_mark_status = models.CharField(max_length=10, null=True)
    selected_justification_code = models.CharField(max_length=1, null=True)
    keying_required = models.CharField(max_length=1, null=True)
    remark_reason = models.TextField(null=True)
    remark_concern_reason = models.TextField(null=True)

class EsmcsvDownloads(models.Model):
    document = models.FileField(upload_to='documents/')
    file_name = models.CharField(max_length=50, null=True)
    download_count = models.CharField(max_length=3, null=True)
    archive_count = models.CharField(max_length=3, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class EarServerSettings(models.Model):
    session_id_list = models.TextField(default='')
    enquiry_id_list = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    session_description = models.TextField(default='')