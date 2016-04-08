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
	doc_number = models.CharField('document number', max_length=50,
									default='QC-001', editable=False)
	doc_title = models.CharField('document title', max_length=100, editable=False,
			default='Interior Component Non-Conformance Worksheet')
	report_number = models.CharField(max_length=50, default="auto", editable=False)
	order_number = models.CharField(max_length=50)

	def __str__(self):
		return self.report_number

	def save(self, *args, **kwargs):
		if self.report_number == 'auto':
			order_date = self.order_number + '-{t:%Y%m%d}'.format(t=datetime.date.today())
			x = IntNCReport.objects.filter(report_number__contains=order_date)
			uid = len(x) + 1
			self.report_number = '{order_date}-{uid}'.format(order_date=order_date, uid=uid)
		super(IntNCReport, self).save(*args, **kwargs)

		

