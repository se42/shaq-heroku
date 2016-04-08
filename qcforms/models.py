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
	locations = [
		('ROADTEST', 'Road Test'),
		('ANALYSISCENTER', 'Analysis Center'),
		('QCAUDIT', 'QZ Audit'),
		('SYNCREON', 'Syncreon'),
		('REWORK', 'Rework'),
		('SECTIONAUDIT', 'Section Audit'),
		('PVAL', 'PVAL'),
		('PRUFRIEGEL', 'Prufriegel Audit'),
		('ASSEMBLY', 'Assembly'),
	]

	parts = [
		('IP', 'Instrument Panel'),
		('CC', 'Center Console'),
		('GB', 'Glove Box'),
		('CCPK', 'Center Console Parts Kit'),
		('CLR', 'Cover Leg Room'),
		('BP', 'Bulk Part'),
		('DPLF', 'Door Panel Left Front'),
		('DPLR', 'Door Panel Left Rear'),
		('DPRF', 'Door Panel Right Front'),
		('DPRR', 'Door Panel Right Rear'),
	]

	inspections = [
		('LUMBEE', '3rd part containment'),
		('BMW', 'Supplier direct containment (initiated by BMW)'),
		('DRX', 'Self directed containment (initiated by DRX)'),
	]

	vehicles = [
		('F15', 'F-15'),
		('F16', 'F-16'),
		('F25', 'F-25'),
		('F26', 'F-26'),
		('F86', 'F-86'),
	]

	drives = [('LHD', 'Left Hand Drive'), ('RHD', 'Right Hand Drive'),]
	shifts = [('A', 'A shift'), ('B', 'B shift'),]

	managers = [
		('DBELL', 'David Bell'),
		('JMITCHELL', 'Jerrica Mitchell'),
	]
	
	doc_number = models.CharField('document number', default='QC-001', editable=False)
	doc_title = models.CharField('document title', editable=False,
			default='Interior Component Non-Conformance Worksheet')
	report_number = models.CharField(default="auto", editable=False)
	order_number = models.CharField()
	vin = models.CharField('VIN')
	build_number = models.CharField()
	report_date = models.DateField()
	issue_summary = models.TextField('non-conformance description')
	location = models.CharField(choices=locations)
	part = models.CharField(choices=parts)
	inspection = models.CharField(choices=inspections)
	vehicle = models.CharField(choices=vehicles)
	drive = models.CharField(choices=drives)
	shift = models.CharField(choices=shifts)
	clean_build = models.CharField(blank=True)
	reported_to = models.CharField(choices=managers)
	repaired = models.BooleanField()
	part_returned = models.BooleanField()

	def __str__(self):
		return self.report_number

	def save(self, *args, **kwargs):
		if self.report_number == 'auto':
			order_date = self.order_number + '-{t:%Y%m%d}'.format(t=datetime.date.today())
			x = IntNCReport.objects.filter(report_number__contains=order_date)
			uid = len(x) + 1
			self.report_number = '{order_date}-{uid}'.format(order_date=order_date, uid=uid)
		super(IntNCReport, self).save(*args, **kwargs)


class IntNCImage(models.Model):
	report = models.ForeignKey('IntNCReport', on_delete=models.CASCADE)
	image_url = models.URLField()

	def __str__(self):
		return self.report.report_number
		

