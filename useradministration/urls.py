from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>((\w+\W*)|(\W+\w*)))/$', views.user_detail),
]
