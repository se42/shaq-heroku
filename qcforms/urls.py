from django.conf.urls import url

from . import views

app_name = 'qcforms'
urlpatterns = [
	url(r'^$', views.QCFormsIndexView.as_view(), name='qcforms_index'),
	url(r'^QC1/$', views.QC1IndexView.as_view(), name='QC1_index'),
	url(r'^QC1/detail/(?P<pk>[0-9]+)/$', views.QC1DetailView.as_view(), name='QC1_detail'),
	url(r'^QC1/form/(?P<report_id>[0-9]+|new\b)/$', views.QC1_report_form, name='QC1_form'),
	url(r'^QAlert/$', views.QualityAlertIndexView.as_view(), name='quality_alert_index'),
	url(r'^QAlert/detail/(?P<pk>[0-9]+)/$', views.QualityAlertDetailView.as_view(),
		name='quality_alert_detail'),
	url(r'^QAlert/form/(?P<report_id>[0-9]+|new\b)/$', views.QualityAlert_report_form,
		name='quality_alert_form'),
	url(r'^amz_sign_s3/$', views.amz_sign_s3, name='amz_sign_s3'),
	url(r'^qcformsjstesting/$', views.qcformsjstesting, name='qcformsjstesting'),
]
