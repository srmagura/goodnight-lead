# Import patterns ant url for registering urls
from django.conf.urls import patterns, url, include

# Import separate view files for linking urls
# to the correct views
from gl_site import views
from gl_site.inventories import views as inventory_views
from gl_site.accounts import views as account_views

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^login$', views.login, name='login'),
    url(r'^register/(?P<session_uuid>[0-9a-f]{32})$', views.register, name='register'),
    url(r'^reset_password$', views.reset_password_page,
        name='reset_password_page'),
    url(r'^logout$', views.logout_user, name='logout'),

    url(r'^account-settings$', account_views.account_settings, name='account-settings'),
    url(r'^account-settings/password$', account_views.password, name='password'),

    url(r'^inventory/take/(?P<inventory_id>[0-9]+)$', inventory_views.take_inventory,
        name='take_inventory'),
    url(r'^inventory/review/(?P<inventory_id>[0-9]+)$', inventory_views.review_inventory,
        name='review_inventory'),

    url(r'^admin', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^set_base_url$', views.set_base_url, name='set_base_url'),

    url(r'^.*$', views.page_not_found, name='page_not_found'),

)
