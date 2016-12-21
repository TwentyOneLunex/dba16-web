from django.conf.urls import url
from . import views

app_name = 'useradministration'
urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^users/reg_user/$', views.show_user_registration_form, name='reg_user'),
    url(r'^users/reg_ok/$', views.registration_successful, name='reg_ok'),
    url(r'^question/$', views.question_get),
    url(r'^question/add/$', views.question_add),
    url(r'^question/answer/$', views.question_answer),
    url(r'^location/$', views.location_get),
    url(r'^location/add/$', views.location_add),
    url(r'^location/weather/add/(?P<pk>[0-9]+)/$', views.weather_add),
    url(r'^users/auth/$', views.auth_check),
    url(r'^users/(?P<pk>((\w+\W*)|(\W+\w*)))/$', views.user_detail),
]
