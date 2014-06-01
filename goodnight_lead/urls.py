from django.conf.urls import patterns, include, url

from app import views
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.login_page, name='login_page'),
    url(r'^do_login$', views.do_login, name='do_login'),
    url(r'^register$', views.register, name='register'),
    url(r'^reset_password_page$', views.reset_password_page, 
        name='reset_password_page'),
    url(r'^logout$', views.logout_user, name='logout'),
    
    #url(r'^admin/', include(admin.site.urls)),
)
