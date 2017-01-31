from django.conf.urls import url
from . import views

app_name = 'coreapp'
urlpatterns = [
    url(r'^users/login_user/$', views.user_login, name='user_login'),
    url(r'^users/eingeloggtView/$', views.user_logout, name='eingeloggt'),
    url(r'^users/$', views.user_list),
    url(r'^users/test/$', views.TestPageView.as_view(), name='test'),
    url(r'^users/myprofile/$', views.show_profile, name='myprofile'),
    url(r'^users/reg_user/$', views.show_user_registration_form, name='reg_user'),
    url(r'^users/reg_ok/$', views.registration_successful, name='reg_ok'),
    url(r'^users/auth/$', views.auth_check),
    url(r'^users/(?P<pk>((\w+\W*)|(\W+\w*)))/$', views.user_detail),
    #url(r'^questionarys/(?P<pk>(\d+))/$', views.questionary_detail),
    url(r'^question/$', views.question_get),
    url(r'^question/add/$', views.question_add),
    url(r'^question/answer/$', views.question_answer),
    url(r'^location/$', views.location_get),
    url(r'^location/add/$', views.location_add),
    url(r'^location/room/add/(?P<pk>[0-9]+)/$', views.room_add),
    url(r'^location/room/$', views.location_room_get),
    url(r'^location/weather/add/(?P<pk>[0-9]+)/$', views.weather_add),
    url(r'^sensor/data/(?P<user>((\w+\W*)|(\W+\w*)))/$', views.sensordata_add),
    url(r'^charts', views.ChartsPageView.as_view(), name='charts'),
    url(r'^index', views.IndexPageView.as_view(), name='index'),
    url(r'^home', views.HomePageView.as_view(), name='home'),
    url(r'^myprofile', views.MyprofilePageView.as_view(), name='profile'),
    url(r'^tables', views.TablesPageView.as_view(), name='tables')
]
