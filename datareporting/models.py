from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Datasets(models.Model):
    dataset_name = models.CharField(max_length=30,null=True)
    last_triggered = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)
    parameter_name = models.CharField(max_length=30,null=True)
    parameter = models.CharField(max_length=30,null=True)
    row_count = models.IntegerField(default=0,null=True)
    error_status = models.CharField(max_length=30,null=True)
    active_refresh = models.BooleanField(default=False,null=True)

class ManualTaskQueue(models.Model):
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name='task_queue')
    task_creation_date = models.DateTimeField(auto_now_add=True)
    task_completion_date = models.DateTimeField(null=True)
    task_queued = models.IntegerField(default=1)
    task_running = models.IntegerField(default=0)

class meps_comp_entries(models.Model):
    centre_id = models.CharField(max_length=8,null=True)
    sap_centre_id = models.CharField(max_length=14,null=True)
    c4c_centre_id = models.CharField(max_length=10,null=True)
    centre_name = models.CharField(max_length=81,null=True)
    cno_postcode = models.CharField(max_length=13,null=True)
    cno_country = models.CharField(max_length=27,null=True)
    cand_uniq_id = models.CharField(max_length=17,null=True)
    school_or_private = models.CharField(max_length=10,null=True)
    cand_ses_id = models.CharField(max_length=7,null=True)
    ses_sid = models.CharField(max_length=8,null=True)
    ses_name = models.CharField(max_length=23,null=True)
    ses_month = models.CharField(max_length=5,null=True)
    ses_year = models.CharField(max_length=7,null=True)
    financial_year = models.CharField(max_length=12,null=True)
    qualif = models.CharField(max_length=7,null=True)
    ass_code = models.CharField(max_length=7,null=True)
    ass_ver_no = models.CharField(max_length=5,null=True)
    opt_code = models.CharField(max_length=5,null=True)
    comp_list = models.CharField(max_length=43,null=True)
    comp_id = models.CharField(max_length=5,null=True)
    kpi_entries_comp = models.CharField(max_length=3,null=True)
    qua_name_sh = models.CharField(max_length=23,null=True)
    ass_name_sh = models.CharField(max_length=33,null=True)
    opt_name = models.CharField(max_length=39,null=True)
    retake_ind = models.CharField(max_length=4,null=True)
    exam_start_date = models.CharField(max_length=24,null=True)
    exam_time_of_day = models.CharField(max_length=4,null=True)
    datetime_received = models.CharField(max_length=24,null=True)
    create_datetime = models.CharField(max_length=24,null=True)
    mod_timestamp = models.CharField(max_length=24,null=True)
    sid = models.CharField(max_length=12,null=True)
    name = models.CharField(max_length=63,null=True)
    sex_code = models.CharField(max_length=4,null=True)
    date_of_birth = models.CharField(max_length=24,null=True)
    national_id = models.CharField(max_length=23,null=True)

class ciedirect_enquiry(models.Model):
    sessid = models.CharField(max_length=8,null=True)
    enquiryid = models.CharField(max_length=10,null=True)
    epsenquiryid = models.CharField(max_length=9,null=True)

class ciedirect_enquirystatus(models.Model):
    enquiryid = models.CharField(max_length=10,null=True)
    enquirystatus = models.CharField(max_length=50,null=True)
    datetime = models.DateTimeField(null=True)

class centre_enquiry_requests(models.Model):
    sid = models.CharField(max_length=10,null=True)
    ses_sid = models.CharField(max_length=8,null=True)
    cnu_id = models.CharField(max_length=8,null=True)
    status = models.CharField(max_length=2,null=True)
    created_datetime = models.DateTimeField(null=True)
    completed_datetime = models.DateTimeField(null=True)

class enquiry_request_parts(models.Model):
    sid = models.CharField(max_length=15,null=True)
    cer_sid = models.CharField(max_length=15,null=True)
    es_service_code = models.CharField(max_length=5,null=True)
    booked_in_error_ind = models.CharField(max_length=5,null=True)

class enquiry_components(models.Model):
    sid = models.CharField(max_length=15,null=True)
    ccm_ass_code = models.CharField(max_length=5,null=True)
    ccm_asv_ver_no = models.CharField(max_length=5,null=True)
    ccm_com_id = models.CharField(max_length=5,null=True)
    erp_sid = models.CharField(max_length=15,null=True)

class all_products(models.Model):
    ses_sid = models.CharField(max_length=15,null=True)
    ass_code = models.CharField(max_length=5,null=True)
    asv_ver_no = models.CharField(max_length=5,null=True)
    com_id = models.CharField(max_length=5,null=True)
    qua_name = models.CharField(max_length=50,null=True)

class Test(models.Model):
    Test = models.CharField(max_length=1,null=True)

class Reports(models.Model):
    report_name = models.CharField(max_length=20,null=True)
    active = models.BooleanField(default=False,null=True)

class Report_Datasets(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE, related_name='datasets')
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name='datasets')
    report_parameter = models.CharField(max_length=20,null=True)