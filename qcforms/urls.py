from django.conf.urls import url

from . import views

app_name = 'qcforms'
urlpatterns = [
	url(r'int-nc/$', views.IntNCIndexView.as_view(), name='int_nc_index'),
	url(r'^int-nc/detail/(?P<pk>[0-9]+)/$', views.IntNCDetailView.as_view(), name='int_nc_detail'),
	url(r'^int-nc/form/(?P<report_id>[0-9]+|new\b)/$', views.int_nc_report_form, name='int_nc_form'),
	# url(r'QC1/$', views.QC1IndexView.as_view(), name='QC1_index'),
	# url(r'^QC1/detail/(?P<pk>[0-9]+)/$', views.QC1DetailView.as_view(), name='QC1_detail'),
	# url(r'^QC1/form/(?P<report_id>[0-9]+|new\b)/$', views.QC1_report_form, name='QC1_form'),
	url(r'^amz_sign_s3/$', views.amz_sign_s3, name='amz_sign_s3'),
	url(r'^qcformsjstesting/$', views.qcformsjstesting, name='qcformsjstesting'),
]
