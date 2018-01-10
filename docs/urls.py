from docs.views import *
from django.conf.urls import url


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^ngs/$', ngs, name='ngs'),
    url(r'^ajax_copy/$', ajax_copy, name='copy'),
    url(r'^training/$', training, name='training'),
    url(r'^general/$', general, name='general'),
    url(r'^ajax_test_docs/$', ajax_test_docs, name='ajax_docs'),
]
