from django.conf.urls import url

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^productions/$', views.production_list),
    url(r'^productions/(?P<pk>[0-9]+)$', views.production_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)