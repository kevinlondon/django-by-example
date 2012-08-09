from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbe.views.home', name='home'),
    # url(r'^dbe/', include('dbe.foo.urls')),

     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^mark_done/(\d*)/$', "todo.views.mark_done"),
     url(r'^delete/(\d*)/$', "todo.views.delete"),
     url(r'^toggle_hold/(\d*)/$', "todo.views.toggle_hold"),
)

