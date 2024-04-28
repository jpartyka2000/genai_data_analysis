from django.conf.urls import patterns, url, include

from satool import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^data-entry/$', views.data_entry, name='dataentry'),
    url(r'^variable-matching/$', views.variable_matching, name='variable_matching'),
    url(r'^term-classification/$', views.term_classification, name='term_classification'),
    url(r'^position-to-profile-matching/$', views.position_to_profile_matching, name='position_to_profile_matching'),
    url(r'^location-classification/$', views.location_classification, name='location_classification'),
    url(r'^study-period/$', views.study_period, name='study_period'),
    url(r'^produce-csv/$', views.produce_csv, name='produce_csv'),
    url(r'^test-download/$', views.test_download, name='test_download'),
    url(r'^profile-popup/$', views.profile_popup, name='profile_popup'),
    url(r'^location-popup/$', views.location_popup, name='location_popup'),
    url(r'^termination-popup/$', views.termination_popup, name='termination_popup'),
    )
