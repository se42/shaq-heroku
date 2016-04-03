from django.forms import ModelForm

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

