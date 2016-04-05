from django.forms import ModelForm
from django.forms.widgets import DateInput, URLInput

from . import models

class IntNCReportBasicForm(ModelForm):
	class Meta:
		model = models.IntNCReportBasic
		fields = [
			'report_number',
			'order_number',
			'vin',
			'report_date',
			'issue_summary',
			'issue_image_url',
		]
		widgets = {
			'report_date': DateInput(attrs={'type': 'date',}),
			'issue_image_url': URLInput(attrs={'type': 'hidden',}),
		}

