from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^update$', 'ddns.views.update', name='update'),
)
