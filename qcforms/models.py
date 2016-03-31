from django.db import models


class ReportBasic(models.Model):
	document_number = models.CharField(max_length=50)

	def __str__(self):
		return self.document_number

class IntNCReportBasic(models.Model):
	order_number = models.CharField(max_length=50)
	vin = models.CharField('VIN', max_length=50)
	report_number = models.CharField(max_length=50)
	report_date = models.DateField()
	issue_summary = models.TextField()
	issue_image = models.ImageField(upload_to='img/')

	def __str__(self):
		return self.report_number
