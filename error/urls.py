from django.conf.urls import patterns, url

urlpatterns = patterns('error.views',
	url(r'^$','handler404'),
)
