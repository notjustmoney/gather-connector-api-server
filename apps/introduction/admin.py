from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = 'contents', 'created_at', 'updated_at', 'is_required',


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = 'contents', 'user', 'answered_at', 'updated_at',
    list_filter = 'user',
