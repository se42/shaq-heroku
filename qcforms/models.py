import datetime

from django.db import models


class ReportBasic(models.Model):
	document_number = models.CharField(max_length=50)
	document_title = models.CharField(max_length=50)

	def __str__(self):
		return self.document_number


class IntNCReportBasic(models.Model):
	order_number = models.CharField(max_length=50)
	vin = models.CharField('VIN', max_length=50)
	report_number = models.CharField(max_length=50)
	report_date = models.DateField()
	issue_summary = models.TextField()
	issue_image_url = models.URLField()

	def __str__(self):
		return self.report_number


class IntNCReport(models.Model):

	def gen_report_num(self):
		date_tag = '{t:%Y%m%d}'.format(t=datetime.datetime.today())
		order_date_pair = self.order_number + '-' + date_tag
		x = IntNCReport.objects.filter(report_number__contains=order_date_pair)
		uid = len(x) + 1
		return '{order}-{t:%Y%m%d}-{uid}'.format(order=self.order_number,
												t=date_tag, uid=uid)

	doc_number = models.CharField('document number', max_length=10,
									default='QC-001', editable=False)
	doc_title = models.CharField('document title', max_length=50, editable=False,
			default='Interior Component Non-Conformance Worksheet')
	report_number = models.CharField(max_length=20, default=gen_report_num, editable=False)
	order_number = models.CharField(max_length=20)

	def __str__(self):
		return self.report_number

	

