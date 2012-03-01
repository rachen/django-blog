from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import logout as django_logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# Examples:
# url(r'^$', 'djblog.views.home', name='home'),
# url(r'^djblog/', include('djblog.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),

urlpatterns = patterns('',
#    url(r'^$', direct_to_template, {"template": "index.html"}, name="index"),
    url(r'^$', "djblog.testblog.views.index"),
    url(r'^accounts/login/$', 'djblog.testblog.views.login', name="login"),
    url(r'^accounts/register/$', 'djblog.testblog.views.register', name="register"),
    url(r'^accounts/logout/$', django_logout, name="logout"),
    url(r'^add_article/$', 'djblog.testblog.views.add_article', name="add_article"),
    url(r'^articles/(\d+)/$', 'djblog.testblog.views.get_article', name="get_article"),
    url(r'^articles/(?P<slug>[-\w]+)/$', 'djblog.testblog.views.get_article_by_slug', name="get_article_by_slug"),
    url(r'^articles/(\d+)/edit$', 'djblog.testblog.views.edit_article', name="edit_article"),
    url(r'^articles/(\d+)/delete$', 'djblog.testblog.views.delete_article', name="delete_article"),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^static_media/(?P<path>.*)$',
         'serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True }),)
