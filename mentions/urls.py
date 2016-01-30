from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^api/v1/api_v1_get_n_mentions_between$',
            views.api_v1_get_n_mentions_between,
            name='api_v1_get_n_mentions_between'
    ),
    url(r'^mention/list/(?P<client_id>\d+)/$', views.mention_list, name='mention_list'),
    url(r'^client/list/$', views.client_list, name='client_list'),
    url(r'^client/add/$', views.client_add, name='client_add'),
    url(r'^$', views.index, name='index'),
]