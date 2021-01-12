from django.contrib import admin
from .models import Song, Keyword, SongRequest, Comment, LikeSong, LikeComment


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = 'title', 'uri',


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = 'name', 'song',


@admin.register(SongRequest)
class SongRequestAdmin(admin.ModelAdmin):
    list_display = 'song', 'user', 'requested_at',


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = 'song', 'contents', 'user', 'created_at',


@admin.register(LikeSong)
class LikeSongAdmin(admin.ModelAdmin):
    list_display = 'song', 'user',


@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):
    list_display = 'comment', 'user',
