from django.forms import ModelForm, inlineformset_factory
from django.forms.widgets import DateInput, Select, URLInput

from . import models


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


class QualityAlertForm(ModelForm):
	class Meta:
		model = models.QualityAlert
		fields = [
			'intncreport',
			'alert_date',
			'issued_by',
			'report_text',
			'complete',
			'resolved',
		]
		widgets = {
			'alert_date': DateInput(attrs={'type': 'date',}),
			'intncreport': Select(attrs={'disabled': 'disabled',}),
		}
