from django.conf.urls import url

from . import views

app_name = 'qcforms'
urlpatterns = [
	# url(r'^$', views.IndexView.as_view(), name='qcforms-index'), # save this base index for later
	url(r'int-nc/$', views.IntNCIndexView.as_view(), name='int-nc-index'),
	url(r'^int-nc/detail/(?P<pk>[0-9]+)/$', views.IntNCDetailView.as_view(), name='int-nc-detail'),
	url(r'^int-nc/form/(?P<report_id>[0-9]+|new\b)/$', views.int_nc_report_form, name='int-nc-form'),
]
