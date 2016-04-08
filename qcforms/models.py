import datetime

from django.db import models


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
	"""
	Model for the QC-001 Interior Component Non-conformance Worksheet
	"""
	locations = [
		('Road Test', 'Road Test'),
		('Analysis Center', 'Analysis Center'),
		('QZ Audit', 'QZ Audit'),
		('Syncreon', 'Syncreon'),
		('Rework', 'Rework'),
		('Section Audit', 'Section Audit'),
		('PVAL', 'PVAL'),
		('Prufriegel Audit', 'Prufriegel Audit'),
		('Assembly', 'Assembly'),
	]

	parts = [
		('Instrument Panel', 'Instrument Panel'),
		('Center Console', 'Center Console'),
		('Glove Box', 'Glove Box'),
		('Center Console Parts Kit', 'Center Console Parts Kit'),
		('Cover Leg Room', 'Cover Leg Room'),
		('Bulk Part', 'Bulk Part'),
		('Door Panel Left Front', 'Door Panel Left Front'),
		('Door Panel Left Rear', 'Door Panel Left Rear'),
		('Door Panel Right Front', 'Door Panel Right Front'),
		('Door Panel Right Rear', 'Door Panel Right Rear'),
	]

	inspections = [
		('3rd part containment (Lumbee)', '3rd part containment (Lumbee)'),
		('Supplier direct containment (initiated by BMW)', 'Supplier direct containment (initiated by BMW)'),
		('Self directed containment (initiated by DRX)', 'Self directed containment (initiated by DRX)'),
	]

	vehicles = [
		('F-15', 'F-15'),
		('F-16', 'F-16'),
		('F-25', 'F-25'),
		('F-26', 'F-26'),
		('F-86', 'F-86'),
	]

	drives = [('Left Hand Drive', 'Left Hand Drive'),
			('Right Hand Drive', 'Right Hand Drive'),]
	shifts = [('A shift', 'A shift'), ('B shift', 'B shift'),]

	managers = [
		('David Bell', 'David Bell'),
		('Jerrica Mitchell', 'Jerrica Mitchell'),
	]

	responsibility = [('Yes', 'Yes'), ('No', 'No'), ('Under Investigation', 'Under Investigation'),]

	BI_levels = [('1','1'), ('2','2'), ('3','3'), ('4','4'),
		('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'),]
	
	doc_number = models.CharField('document number', max_length=250, default='QC-001', editable=False)
	doc_title = models.CharField('document title', max_length=250, editable=False,
			default='Interior Component Non-Conformance Worksheet')
	report_number = models.CharField(max_length=250, default="auto", editable=False)
	order_number = models.CharField(max_length=250)
	vin = models.CharField('VIN', max_length=250)
	build_number = models.CharField(max_length=250)
	report_date = models.DateField(default=datetime.date.today)
	issue_summary = models.TextField('non-conformance description')
	location = models.CharField(max_length=250, choices=locations)
	part = models.CharField(max_length=250, choices=parts)
	inspection = models.CharField(max_length=250, choices=inspections)
	vehicle = models.CharField(max_length=250, choices=vehicles)
	drive = models.CharField(max_length=250, choices=drives)
	shift = models.CharField(max_length=250, choices=shifts)
	clean_build = models.CharField(max_length=250, blank=True)
	reported_to = models.CharField(max_length=250, choices=managers)
	repaired = models.BooleanField()
	part_returned = models.BooleanField()
	BI_level = models.CharField(max_length=250, choices=BI_levels, blank=True)
	in_PCSQ = models.BooleanField()
	qn_num = models.CharField(max_length=250, blank=True)
	accepts = models.CharField(max_length=250, choices=responsibility, default='Under Investigation')
	containment = models.BooleanField()
	quality_alert = models.BooleanField()
	containment_activity = models.TextField(blank=True)
	additional_info = models.TextField(blank=True)
	internal_rep = models.CharField(max_length=250)
	external_rep = models.CharField(max_length=250)
	resolved = models.BooleanField(default=False)


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
		

