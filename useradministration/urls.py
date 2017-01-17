from django.conf.urls import url
from . import views

app_name = 'useradministration'
urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^users/test/$', views.TestPageView.as_view(), name='test'),
    url(r'^users/myprofile/$', views.show_profile, name='myprofile'),
    url(r'^users/reg_user/$', views.show_user_registration_form, name='reg_user'),
    url(r'^users/reg_ok/$', views.registration_successful, name='reg_ok'),
    url(r'^questionarys/$', views.questionary_list),
    url(r'^users/auth/$', views.auth_check),
    url(r'^users/(?P<pk>((\w+\W*)|(\W+\w*)))/$', views.user_detail),
    url(r'^questionarys/(?P<pk>(\d+))/$', views.questionary_detail),
]
