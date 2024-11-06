from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import AllSessions, PDQSessions
from django import forms

class ResultsDateForm(forms.ModelForm):
    class Meta:
        model = PDQSessions
        fields = ['results_release_datetime']
        widgets = {
            'results_release_datetime': DateTimePickerInput(options={
            "format": "DD/MM/YYYY HH:mm:ss",
            "showTodayButton": True,
        },),
        }
