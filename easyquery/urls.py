from django.urls import path, include
from . import views

app_name = "easyquery"

urlpatterns = [
    path('', views.index_v1, name='index_v1'),
    path('create_new_study/', views.create_new_study, name='create_new_study'),
    path('answer_user_question/', views.answer_user_question, name='answer_user_question'),
    path('history/', views.history_list, name='history'),
    #path('history/<int:pk>', views.history_detail, name='history_detail'),
    #path('v1', views.index_v1, name='indexv1'),
    path('create_new_study/v1', views.create_new_study_v1, name='create_new_study_v1'),
    path('answer_user_question/v1', views.answer_user_question_v1, name='answer_user_question_v1'),
    #path('v1/todolist/teams', views.to_do_list_teams, name='to_do_list_teams'),
    #path('v1/todolist/roadmap', views.to_do_list_roadmap, name='to_do_list_roadmap'),
    #path('v1/todolist/questions', views.to_do_list_questions, name='to_do_list_questions'),
    path('export_data/', views.export_data, name='export_data'),
    #path("create_new_study/", views.create_new_study, name='create_new_study'),
    #path(r'answer_user_question/$', views.answer_user_question, name='answer_user_question')
]
