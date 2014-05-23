from django.conf.urls import patterns, include, url

from app import views
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.login_page, name='login_page'),
    url(r'^do_login$', views.do_login, name='do_login'),

    #url(r'^admin/', include(admin.site.urls)),
)
