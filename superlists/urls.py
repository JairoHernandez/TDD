from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import include, url
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),
    # url(r'^admin/', include(admin.site.urls)),
]


# 'name' value is used by {% url %} template tag in html file
# url(r'^admin/', include(admin.site.urls)),
