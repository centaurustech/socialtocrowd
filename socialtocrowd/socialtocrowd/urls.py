from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('landing.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', 'userprofile.views.profile', name="profile"),
    url(r'^profile/', include('userprofile.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
