from django.urls import path
from .views import (QuestionListAPIView, QuestionDetailAPIView,
                    AnswerListAPIView, AnswerDetailAPIView)

urlpatterns = [
    path(r'questions/', QuestionListAPIView.as_view()),
    path(r'questions/<int:pk>', QuestionDetailAPIView.as_view(), name='question-detail'),
    path(r'answers/', AnswerListAPIView.as_view(), name='answer-list'),
    path(r'answers/<int:pk>', AnswerDetailAPIView.as_view(), name='answer-detail'),
]
