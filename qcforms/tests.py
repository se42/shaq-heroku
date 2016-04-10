import datetime

from django.test import TestCase

from . import models

class IntNCReportTestCase(TestCase):
	def setUp(self):
		self.date_tag = '{t:%Y%m%d}'.format(t=datetime.date.today())
		models.IntNCReport.objects.create(order_number='ORD1',
											vin='1FTRX12W78FB43241',
											build_number='34590834',
											issue_summary='Something bad has happened',
											location='Road Test',
											part='Bulk Part',
											inspection='Self directed containment (initiated by DRX)',
											vehicle='F-15',
											drive='Left Hand Drive',
											shift='A shift',
											reported_to='David Bell',
											repaired=False,
											part_returned=False,
											BI_level='5',
											in_PCSQ=False,
											containment=False,
											quality_alert=True,
											internal_rep='Some Guy',
											external_rep='Some Girl',
											resolved=True,
		)
		models.IntNCReport.objects.create(order_number='ORD1',
											vin='JB3BA34KXGU004676',
											build_number='34590834',
											issue_summary='Something bad has happened',
											location='Road Test',
											part='Bulk Part',
											inspection='Self directed containment (initiated by DRX)',
											vehicle='F-15',
											drive='Left Hand Drive',
											shift='A shift',
											reported_to='David Bell',
											repaired=False,
											part_returned=False,
											BI_level='5',
											in_PCSQ=False,
											containment=False,
											quality_alert=True,
											internal_rep='Some Guy',
											external_rep='Some Girl',
											resolved=True,
		)
		models.IntNCReport.objects.create(order_number='ORD2',
											vin='4UZ6CJBA7YCG86866',
											build_number='34590834',
											issue_summary='Something bad has happened',
											location='Road Test',
											part='Bulk Part',
											inspection='Self directed containment (initiated by DRX)',
											vehicle='F-15',
											drive='Left Hand Drive',
											shift='A shift',
											reported_to='David Bell',
											repaired=False,
											part_returned=False,
											BI_level='5',
											in_PCSQ=False,
											containment=False,
											quality_alert=True,
											internal_rep='Some Guy',
											external_rep='Some Girl',
											resolved=True,
		)

	def test_report_number_generation(self):
		ORD1_list = list(models.IntNCReport.objects.filter(order_number='ORD1'))
		ORD2_list = list(models.IntNCReport.objects.filter(order_number='ORD2'))
		ORD1_rep_nums = [x.report_number for x in ORD1_list]
		ORD2_rep_nums = [x.report_number for x in ORD2_list]
		ORD1_number_1 = 'ORD1-' + self.date_tag + '-1'
		ORD1_number_2 = 'ORD1-' + self.date_tag + '-2'
		ORD2_number_1 = 'ORD2-' + self.date_tag + '-1'

		self.assertTrue(ORD1_number_1 in ORD1_rep_nums, "ORD1-date-1 not in ORD1 report numbers")
		self.assertTrue(ORD1_number_2 in ORD1_rep_nums, "ORD1-date-2 not in ORD1 report numbers")
		self.assertTrue(ORD2_number_1 in ORD2_rep_nums, "ORD2-date-1 not in ORD2 report numbers")


