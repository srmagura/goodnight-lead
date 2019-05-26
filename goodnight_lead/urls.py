"""
Define all of the URL patterns for the site.
"""

# Import patterns ant url for registering urls
from django.conf.urls import url, include

# Import separate view files for linking urls
# to the correct views
from gl_site import views
from gl_site.inventories import views as inventory_views
from gl_site.accounts import views as account_views
from gl_site.statistics import views as statistic_views

from django.contrib import admin

urlpatterns = [
    # Dashboard
    url(r'^$', views.dashboard, name='dashboard'),

    # User sign in / registration
    url(r'^login$', views.login, name='login'),
    url(r'^register/(?P<session_uuid>[0-9a-f]{32})$', views.register, name='register'),
    url(r'^reset_password$', views.reset_password_page,
        name='reset_password_page'),
    url(r'^logout$', views.logout_user, name='logout'),

    # Account settings
    url(r'^account-settings$', account_views.account_settings, name='account-settings'),
    url(r'^account-settings/password$', account_views.password, name='password'),

    # Take inventory and review inventory pages
    url(r'^inventory/take/(?P<inventory_id>[0-9]+)$', inventory_views.take_inventory,
        name='take_inventory'),
    url(r'^inventory/review/(?P<inventory_id>[0-9]+)$', inventory_views.review_inventory,
        name='review_inventory'),

    # Statistics functionality
    url(r'^statistics/view$', statistic_views.view_statistics, name='view_statistics'),
    url(r'^statistics/load_data$', statistic_views.load_data, name='load_data'),
    url(r'^statistics/download_data$', statistic_views.download_data, name='download_data'),

    # Admin site
    url(r'^admin', admin.site.urls),
    url(r'^set_base_url$', views.set_base_url, name='set_base_url'),

    # Catch-all for URLs that do not match any of the above patterns
    url(r'^.*$', views.page_not_found, name='page_not_found'),
]
