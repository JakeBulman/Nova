from django.db import models
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class AllSessions(models.Model):
    session_id = models.CharField(max_length=5)
    session_name = models.TextField(null=True,default=None)
    session_year = models.IntegerField(null=True,default=None)
    session_sequence = models.IntegerField(null=True,default=None)

    class Meta:
        ordering = ["session_year","session_sequence"]

class PDQSessions(models.Model):
    session_id = models.CharField(max_length=5, unique=True)
    session_name = models.TextField(null=True,default=None)
    session_year = models.IntegerField(null=True,default=None)
    session_sequence = models.IntegerField(null=True,default=None)
    results_release_datetime = models.DateTimeField()
    visible_session = models.IntegerField(default=1)

    class Meta:
        ordering = ["session_year","session_sequence"]

class PDQEntries(models.Model):
    session_id = models.ForeignKey(PDQSessions, to_field='session_id', on_delete=models.CASCADE, related_name='session_entries')
    centre_number = models.CharField(max_length=5)
    candidate_id = models.CharField(max_length=6)
    syllabus_code = models.CharField(max_length=4)
    component_id = models.CharField(max_length=2)
    syllabus_grade = models.CharField(max_length=3)


    class Meta:
        ordering = ["session_id","centre_number"]

class PDQStage(models.Model):
    entry = models.OneToOneField(PDQEntries, on_delete=models.CASCADE, related_name='entry_stage')
    #add new stages to workflow here
    csv_download = models.BooleanField(default=False)


    class Meta:
        ordering = ["entry"]