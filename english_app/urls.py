from django.urls import path, include

from english_app import views

app_name = 'english_app'


api_conf_module = [
    path('random_word/', views.RandomWord.as_view(), name='random_word_api'),
    path('random_exam/', views.RandomExam.as_view(), name='random_exam_api'),
    path('history_exam/', views.ExaminationView.as_view(), name='history_exam_api'),
    path('history_exam/<int:pk>/', views.ExaminationDetailView.as_view(), name='examinationmodel-detail'),
]


urlpatterns = [
    path('', views.index, name='index'),
    path('random_word/', views.random_word, name='random_word'),
    path('all_words/', views.all_words, name='all_words'),
    path('add_word/', views.add_word, name='add_word'),
    path('random_exam/', views.random_exam, name='random_exam'),
    path('history_exam/', views.history_exam, name='history_exam'),


    path('words/', views.WordListView.as_view(), name='wordmodel-list'),
    path('words/<int:pk>/', views.WordDetailView.as_view(), name='wordmodel-detail'),


    path('api/', include(api_conf_module)),
]


