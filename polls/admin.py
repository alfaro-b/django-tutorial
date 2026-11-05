from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["id", "question_text", "pub_date", "was_published_recently"]
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
