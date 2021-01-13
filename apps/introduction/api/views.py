from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Question, Answer

from .serializers import QuestionSerializer, AnswerSerializer
from apps.common.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUserOrReadOnly, IsAuthenticated,)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        question_id = self.request.data['question']
        question = get_object_or_404(Question, pk=question_id)
        serializer.save(user=self.request.user, question=question)
