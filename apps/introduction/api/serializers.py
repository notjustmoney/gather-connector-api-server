from rest_framework import serializers
from ..models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    question = serializers.HyperlinkedRelatedField(read_only=True, view_name='question-detail')

    class Meta:
        model = Answer
        fields = '__all__'
