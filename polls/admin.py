from django.contrib import admin

from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question_text", "pub_date"]
    list_filter = ["pub_date"]
    ordering = ["-pub_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "choice_text", "votes"]
    list_filter = ["question", "choice_text", "votes"]
    ordering = ["id"]
    search_fields = ["id", "question__question_text", "choice_text", "votes"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
