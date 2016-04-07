import datetime

from django.test import TestCase

from . import models

class IntNCReportTestCase(TestCase):
	def setUp(self):
		self.mydate = datetime.date(2016, 5, 5)
		self.date_tag = '{t:%Y%m%d}'.format(t=self.mydate)
		IntNCReport.objects.create(order_number='O-123')
		IntNCReport.objects.create(order_number='O-123')
		IntNCReport.objects.create(order_number='O-234')

	def test_gen_report_num(self):
		order_123_pair = 'O-123-20160505'
		order_234_pair = 'O-234-20160505'

		order_123_1 = IntNCReport.objects.filter(order_number='O-123')
		order_234_1 = IntNCReport.objects.filter(order_number='O-234')
		order_123_2 = IntNCReport.objects.fitler(report_number__contains=order_123_pair)
		order_234_2 = IntNCReport.objects.fitler(report_number__contains=order_234_pair)

		order_123_rep_nums = [x.report_number for x in order_123]
		order_123_r1 = order_123_pair + '-1'
		order_123_r2 = order_123_pair + '-2'
		order_234_r1 = order_234_pair + '-1'

		self.assertEqual(self.date_tag, '20160505', "Date tag not formatted as expected.")
		self.assertEqual(order_123_1, order_123_2, "O-123 filter methods not equal.")
		self.assertEqual(order_234_1, order_234_2, "O-234 filter methods not equal.")
		self.assertTrue(order_123_r1 in order_123_rep_nums, "O-123-date-1 not in O-123 report numbers")
		self.assertTrue(order_123_r2 in order_123_rep_nums, "O-123-date-2 not in O-123 report numbers")
		self.assertTrue(order_234_r1 in order_234_rep_nums, "O-234-date-1 not in O-234 report numbers")


