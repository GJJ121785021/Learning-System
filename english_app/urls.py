from django.urls import path, include
from django.views.generic import TemplateView

from english_app import views

app_name = 'english_app'


api_conf_module = [
    path('random_word/', views.RandomWord.as_view(), name='random_word_api'),
    path('random_exam/', views.RandomExam.as_view(), name='random_exam_api'),
    path('history_exam/', views.ExaminationView.as_view(), name='history_exam_api'),
    path('history_exam/<int:pk>/', views.ExaminationDetailView.as_view(), name='examinationmodel-detail'),
]


urlpatterns = [
    path('', TemplateView.as_view(template_name='english_app/index.html'), name='index'),
    path('random_word/', TemplateView.as_view(template_name='english_app/random_word.html'), name='random_word'),
    path('all_words/', TemplateView.as_view(template_name='english_app/all_words.html'), name='all_words'),
    path('add_word/', TemplateView.as_view(template_name='english_app/add_word.html'), name='add_word'),
    path('random_exam/', TemplateView.as_view(template_name='english_app/random_exam.html'), name='random_exam'),
    path('history_exam/', TemplateView.as_view(template_name='english_app/history_exam.html'), name='history_exam'),


    path('words/', views.WordListView.as_view(), name='wordmodel-list'),
    path('words/<int:pk>/', views.WordDetailView.as_view(), name='wordmodel-detail'),


    path('api/', include(api_conf_module)),
]


