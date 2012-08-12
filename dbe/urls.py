from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbe.views.home', name='home'),
    # url(r'^dbe/', include('dbe.foo.urls')),

     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^item_action/(done|delete|onhold)/(\d*)/$', "todo.views.item_action"),
)

urlpatterns += patterns("blog.views",
    url(r'^$', 'main'),
    url(r'^(\d+)/$', 'post'),
    url(r'^add_comment/(\d+)/$', 'add_comment'),
    url(r'^month/(\d+)/(\d+)/$', 'month'),
    url(r'^delete_comment/(\d+)/$', 'delete_comment'),
    url(r'^delete_comment/(\d+)/(\d+)/$', 'delete_comment'),
)

