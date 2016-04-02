import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from . import models, forms


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
		file_dict = request.FILES
		t = datetime.date.today()
		year = t.year
		month = t.month
		day = t.day
		rnum = request.POST['report_number']
		for each in file_dict.keys():
			file_dict[each].name = '{y}{m}{d}-{r}-'.format(
				y=year, m=month, d=day, r=rnum) + file_dict[each].name

		if report_id == 'new':
			form = forms.IntNCReportBasicForm(request.POST, file_dict)
			report = form.save()
			return HttpResponseRedirect(reverse('qcforms:int-nc-detail', args=(report.id,)))
		else:
			report = get_object_or_404(models.IntNCReportBasic, pk=report_id)
			form = forms.IntNCReportBasicForm(request.POST, file_dict, instance=report)
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

