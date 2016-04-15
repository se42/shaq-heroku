import base64
import datetime
import hmac
import json
import os
import time
import urllib.parse
from hashlib import sha1

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from shaq.utils import active_and_login_required
from . import models, forms


class QCFormsIndexView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
	"""
	Index view to display all available QC forms
	"""
	template_name = 'qcforms/QCForms_index.html'
	context_object_name = 'url_list'

	def get_queryset(self):
		url_list = [
			{
				'view': reverse('qcforms:QC1_index'),
				'name': 'QC-001 Interior Component NC Index',
			},
			{
				'view': reverse('qcforms:quality_alert_index'),
				'name': 'QC-002 Quality Alert',
			},
			{
				'view': "#",
				'name': 'Form 3',
			},
		]
		return url_list

	def test_func(self):
		return self.request.user.is_active

###############################################
# QC-001 / Interior Component NC views

class QC1IndexView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
	"""
	Index view to display all instances of the Interior Component NC Form
	"""
	template_name = 'qcforms/QC1_index.html'
	context_object_name = 'report_list'

	def get_queryset(self):
		return models.IntNCReport.objects.order_by('report_number')

	def test_func(self):
		return self.request.user.is_active


class QC1DetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
	"""
	Detail view to display specific instances of the Interior Component NC Form
	"""
	model = models.IntNCReport
	template_name = 'qcforms/QC1_detail.html'
	context_object_name = 'report'

	def test_func(self):
		return self.request.user.is_active

@active_and_login_required
def QC1_report_form(request, report_id):
	if request.method == 'POST':
		if report_id == 'new':
			form = forms.IntNCReportForm(request.POST)
			if form.is_valid():
				report = form.save()
				formset = forms.IntNCImageInlineFormset(request.POST, instance=report)
				if formset.is_valid():
					formset.save()
			return HttpResponseRedirect(reverse('qcforms:QC1_detail', args=(report.id,)))
		else:
			report = get_object_or_404(models.IntNCReport, pk=report_id)
			form = forms.IntNCReportForm(request.POST, instance=report)
			formset = forms.IntNCImageInlineFormset(request.POST, instance=report)
			if form.is_valid() and formset.is_valid():
				report = form.save()
				formset.save()
			return HttpResponseRedirect(reverse('qcforms:QC1_detail', args=(report.id,)))
	else:
		if report_id == 'new':
			form = forms.IntNCReportForm()
			formset = forms.IntNCImageInlineFormset()
			context = {
				'form': form,
				'formset': formset,
				'report_id': report_id,
			}
			return render(request, 'qcforms/QC1_form.html', context)
		else:
			report = get_object_or_404(models.IntNCReport, pk=report_id)
			form = forms.IntNCReportForm(instance=report)
			formset = forms.IntNCImageInlineFormset(instance=report)
			context = {
				'form': form,
				'formset': formset,
				'report_id': report_id,
			}
			return render(request, 'qcforms/QC1_form.html', context)


###############################################
# QC-002 / Quality Alert views

class QualityAlertIndexView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
	"""
	Index view to display all instances of the Interior Component NC Form
	"""
	template_name = 'qcforms/quality_alert_index.html'
	context_object_name = 'report_list'

	def get_queryset(self):
		return models.QualityAlert.objects.order_by('report_number')

	def test_func(self):
		return self.request.user.is_active


class QualityAlertDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
	"""
	Detail view to display specific instances of the Quality Alert Form
	"""
	model = models.QualityAlert
	template_name = 'qcforms/quality_alert_detail.html'
	context_object_name = 'report'

	def test_func(self):
		return self.request.user.is_active

@active_and_login_required
def QualityAlert_report_form(request, report_id):
	if request.method == 'POST':
		if report_id == 'new':
			form = forms.QualityAlertForm(request.POST)
			if form.is_valid():
				report = form.save()
			return HttpResponseRedirect(reverse('qcforms:quality_alert_detail', args=(report.id,)))
		else:
			report = get_object_or_404(models.QualityAlert, pk=report_id)
			form = forms.QualityAlertForm(request.POST, instance=report)
			if form.is_valid():
				report = form.save()
			return HttpResponseRedirect(reverse('qcforms:quality_alert_detail', args=(report.id,)))
	else:
		if report_id == 'new':
			try:
				intnc_id = request.GET['intnc_id']
			except KeyError:
				intnc_id = None
			form = forms.QualityAlertForm()
			context = {
				'form': form,
				'report_id': report_id,
				'intnc_id': intnc_id,
			}
			return render(request, 'qcforms/quality_alert_form.html', context)
		else:
			report = get_object_or_404(models.QualityAlert, pk=report_id)
			form = forms.QualityAlertForm(instance=report)
			context = {
				'form': form,
				'report_id': report_id,
			}
			return render(request, 'qcforms/quality_alert_form.html', context)


#########################
# S3 signature processing

@active_and_login_required
def amz_sign_s3(request):
	"""
	View for issuing signed requests to PUT/GET resources on S3.  Behavior
	depends on which parameters are passed in the URL.  Use a URL template
	tag at the bottom of the corresponding HTML page to define var amz_s3_url
	pointing to this view.

	To obtain a signature to PUT a file on S3 use the following xhr.open statement:

		xhr.open("GET", sign_s3_url+"?file_name="+file.name+"&file_type="+file.type+"&folder=int-nc-form");

	To obtain a signature to GET a private file from S3 use the following xhr.open:

		xhr.open("GET", amz_s3_url+"?resource_url="+resource_url);

	"""
	PUT_conditions = [
		'file_name' in request.GET,
		'file_type' in request.GET,
		'folder' in request.GET,
	]

	GET_conditions = [
		'resource_url' in request.GET,
	]

	if all(PUT_conditions):
		allowed_types = ['image/jpeg', 'image/png']
		if request.GET['file_type'] in allowed_types:
			return _amz_sign_s3_PUT(request)
		else:
			return None
	elif all(GET_conditions):
		return _amz_sign_s3_GET(request)
	else:
		return None

def _amz_sign_s3_GET(request):
	url = request.GET['resource_url']
	prefix = 'https://s3.amazonaws.com'
	uri = url[len(prefix):]
	expires = _amz_sig_expires()

	string_to_sign = "GET\n\n\n{exp}\n{uri}".format(exp=expires, uri=uri)
	signature = _amz_create_signature(string_to_sign)

	return _amz_signed_request_json(url, expires, signature)

def _amz_sign_s3_PUT(request):
	AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']
	bucket = AWS_S3_BUCKET + '/' + request.GET['folder']

	mime_type = request.GET['file_type']
	fname = urllib.parse.quote_plus(request.GET['file_name'])
	fname = '{t:%Y%m%d%H%M%S}-{f}'.format(t=datetime.datetime.today(), f=fname)
	expires = _amz_sig_expires()
	url = 'https://s3.amazonaws.com/{bucket}/{name}'.format(bucket=bucket, name=fname)

	string_to_sign = "PUT\n\n{mime}\n{exp}\n/{bucket}/{name}".format(
		mime=mime_type, exp=expires, bucket=bucket, name=fname)
	signature = _amz_create_signature(string_to_sign)

	return _amz_signed_request_json(url, expires, signature)

def _amz_sig_expires():
	return int(time.time()+60*60*24)

def _amz_create_signature(string_to_sign):
	AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

	encodedSecretKey = AWS_SECRET_KEY.encode()
	encodedString = string_to_sign.encode()
	h = hmac.new(encodedSecretKey, encodedString, sha1)
	hDigest = h.digest()
	signature = base64.encodebytes(hDigest).strip()
	signature = urllib.parse.quote_plus(signature)

	return signature

def _amz_signed_request_json(url, expires, signature):
	AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']

	return JsonResponse({
		'signed_request': '{url}?AWSAccessKeyId={key}&Expires={exp}&Signature={sig}'.format(
			url=url, key=AWS_ACCESS_KEY, exp=expires, sig=signature),
		'url': url,
	})


#########################
# Views to render Javascript testing HTML pages
@active_and_login_required
def qcformsjstesting(request):
	return render(request, 'qcforms/test_templates/qcforms_tests.html')


