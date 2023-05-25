from django import forms

from .models import Enquiries

class EnquiriesForm(forms.ModelForm):

	class Meta:
		model = Enquiries
		fields = "__all__"

class IECForm(forms.ModelForm):

	class Meta:
		model = Enquiries
		fields = "__all__"

