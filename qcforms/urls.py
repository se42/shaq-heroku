from django.conf.urls import url

from . import views

app_name = 'qcforms'
urlpatterns = [
	# url(r'^$', views.IndexView.as_view(), name='qcforms_index'), # save this base index for later
	url(r'int-nc/$', views.IntNCIndexView.as_view(), name='int_nc_index'),
	url(r'^int-nc/detail/(?P<pk>[0-9]+)/$', views.IntNCDetailView.as_view(), name='int_nc_detail'),
	url(r'^int-nc/form/(?P<report_id>[0-9]+|new\b)/$', views.int_nc_report_form, name='int_nc_form'),
	url(r'^int-nc/sign-s3/$', views.int_nc_sign_s3, name='int_nc_sign_s3'),
	url(r'^sign_s3_GET/$', views.sign_s3_GET, name='sign_s3_GET'),
]
