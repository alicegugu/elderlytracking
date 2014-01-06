from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_test.views.home', name='home'),
    
	url(r'^accounts/', include('userprofile.urls')),

	
    url(r'^admin/', include(admin.site.urls)),
	url(r'^hello_template/$', 'article.views.hello_template'),
	url(r'^accounts/login/$', 'django_test.views.login'),
	url(r'^accounts/auth/$', 'django_test.views.auth_view'),
	url(r'^accounts/logout/$', 'django_test.views.logout'),
	url(r'^accounts/loggedin/$', 'django_test.views.loggedin'),
	url(r'^accounts/invalid/$', 'django_test.views.invalid_login'),
	url(r'^accounts/register/$', 'django_test.views.register_user'),
	url(r'^accounts/register_success/$', 'django_test.views.register_success'),
	url(r'^set_position$', 'django_test.views.set_position'),
	url(r'^get_position$', 'django_test.views.get_position'),
	url(r'^set_gps_position$', 'django_test.views.set_gps_position'),
	url(r'^indoor_tracking$', 'django_test.views.indoor_tracking'),
	url(r'^outdoor_tracking$', 'django_test.views.outdoor_tracking'),
	url(r'^alert$', 'django_test.views.alert'),
	url(r'^end_call$', 'django_test.views.end_call'),
	url(r'^api/alert/$','django_test.views.alert_api')
	)
