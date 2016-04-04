import datetime

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from . import models, forms

import time, os, json, base64, hmac, urllib.parse
from hashlib import sha1


class IndexView(generic.ListView):
	"""
	Index view to display all available QC forms.
	"""
	template_name = 'qcforms/qcforms-index.html'
	context_object_name = 'report_list'

	def get_queryset(self):
		return models.ReportBasic.objects.order_by('document_number')


class IntNCReportDeleteView(generic.edit.DeleteView):
	"""
	Generic delete view.  Provide template_name and success_url as
	arguments in the as_view() function within the url.
	"""
	model = models.IntNCReportBasic
	template_name = None # 'qcforms/delete.html'
	success_url = None # reverse_lazy('qcforms:index')


class IntNCIndexView(generic.ListView):
	"""
	Index view to display all instances of the Interior Component NC Form
	"""
	template_name = 'qcforms/int-nc-index.html'
	context_object_name = 'report_list'

	def get_queryset(self):
		return models.IntNCReportBasic.objects.order_by('report_date')


class IntNCDetailView(generic.DetailView):
	"""
	Detail view to display specific instances of the Interior Component NC Form
	"""
	model = models.IntNCReportBasic
	template_name = 'qcforms/int-nc-detail.html'


def int_nc_report_form(request, report_id):
	if request.method == 'POST':
		if report_id == 'new':
			form = forms.IntNCReportBasicForm(request.POST)
			report = form.save()
			return HttpResponseRedirect(reverse('qcforms:int-nc-detail', args=(report.id,)))
		else:
			report = get_object_or_404(models.IntNCReportBasic, pk=report_id)
			form = forms.IntNCReportBasicForm(request.POST, instance=report)
			report = form.save()
			return HttpResponseRedirect(reverse('qcforms:int-nc-detail', args=(report.id,)))
	else:
		if report_id == 'new':
			form = forms.IntNCReportBasicForm()
			context = {
				'form': form,
				'report_id': report_id,
			}
			return render(request, 'qcforms/int-nc-report-form.html', context)
		else:
			report = get_object_or_404(models.IntNCReportBasic, pk=report_id)
			form = forms.IntNCReportBasicForm(instance=report)
			context = {
				'form': form,
				'report_id': report_id,
			}
			return render(request, 'qcforms/int-nc-report-form.html', context)

def int_nc_sign_s3(request):
	AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
	AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
	AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']

	mime_type = request.GET['file_type']
	allowed_types = ['image/jpeg', 'image/png']

	if mime_type in allowed_types:
		object_name = urllib.parse.quote_plus(request.GET['file_name'])
		object_name = '{t:%Y%m%d%H%M%S}-{f}'.format(t=datetime.datetime.today(), f=object_name)

		expires = int(time.time()+60*60*24)
		# amz_headers = "x-amz-acl:public-read"

		string_to_sign = "PUT\n\n{mime}\n{exp}\n/{bucket}/int-nc-form/{name}".format(
			mime=mime_type, exp=expires, bucket=AWS_S3_BUCKET, name=object_name)

		encodedSecretKey = AWS_SECRET_KEY.encode()
		encodedString = string_to_sign.encode()
		h = hmac.new(encodedSecretKey, encodedString, sha1)
		hDigest = h.digest()
		signature = base64.encodebytes(hDigest).strip()
		signature = urllib.parse.quote_plus(signature)
		url = 'https://s3.amazonaws.com/{bucket}/int-nc-form/{name}'.format(
			bucket=AWS_S3_BUCKET, name=object_name)

		return JsonResponse({
			'signed_request': '{url}?AWSAccessKeyId={key}&Expires={exp}&Signature={sig}'.format(
				url=url, key=AWS_ACCESS_KEY, exp=expires, sig=signature),
			'url': url,
		})
	else:
		return None

def sign_s3_GET(request):
	AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
	AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
	AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']
	full_url = request.GET['resource_url']

	prefix = 'https://s3.amazonaws.com'
	uri = full_url[len(prefix):]

	# mime_type = request.GET['file_type']
	# allowed_types = ['image/jpeg', 'image/png']

	# object_name = urllib.parse.quote_plus(request.GET['file_name'])
	# object_name = '{t:%Y%m%d%H%M%S}-{f}'.format(t=datetime.datetime.today(), f=object_name)

	expires = int(time.time()+60*60*24)
	# amz_headers = "x-amz-acl:public-read"

	string_to_sign = "GET\n\n\n{exp}\n{uri}".format(exp=expires, uri=uri)

	encodedSecretKey = AWS_SECRET_KEY.encode()
	encodedString = string_to_sign.encode()
	h = hmac.new(encodedSecretKey, encodedString, sha1)
	hDigest = h.digest()
	signature = base64.encodebytes(hDigest).strip()
	signature = urllib.parse.quote_plus(signature)
	# url = 'https://s3.amazonaws.com/{bucket}/int-nc-form/{name}'.format(
	# 	bucket=AWS_S3_BUCKET, name=object_name)

	return JsonResponse({
		'signed_request': '{url}?AWSAccessKeyId={key}&Expires={exp}&Signature={sig}'.format(
			url=full_url, key=AWS_ACCESS_KEY, exp=expires, sig=signature),
		'url': full_url,
	})





