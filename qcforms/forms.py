from django.forms import ModelForm, inlineformset_factory
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


class IntNCReportForm(ModelForm):
	class Meta:
		model = models.IntNCReport
		fields = [
			'order_number',
			'build_number',
			'vin',
			'report_date',
			'issue_summary',
			'location',
			'part',
			'inspection',
			'vehicle',
			'drive',
			'shift',
			'clean_build',
			'repaired',
			'part_returned',
			'BI_level',
			'in_PCSQ',
			'qn_num',
			'accepts',
			'containment',
			'quality_alert',
			'containment_activity',
			'additional_info',
			'internal_rep',
			'external_rep',
			'reported_to',
			'resolved',
		]
		widgets = {
			'report_date': DateInput(attrs={'type': 'date',}),
		}

IntNCImageInlineFormset = inlineformset_factory(
	models.IntNCReport,
	models.IntNCImage,
	fields=('image_url',),
	widgets={'image_url': URLInput(attrs={'type': 'hidden',}),},
	extra=0,
	can_delete=False,
)
