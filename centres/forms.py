from django import forms

from .models import Centres

class CentresForm(forms.ModelForm):

	class Meta:
		model = Centres
		fields = "__all__"
