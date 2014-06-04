from django.conf.urls import patterns, include, url

from app import views
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^login$', views.login_page, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^reset_password$', views.reset_password_page, 
        name='reset_password_page'),
    url(r'^logout$', views.logout_user, name='logout'),
    
    url(r'^inventory/(?P<inventory_id>[0-9]+)/$', views.take_inventory,
        name='take_inventory'),
        
    url(r'^.*$', views.page_not_found, name='page_not_found'),

    #url(r'^admin/', include(admin.site.urls)),
)
