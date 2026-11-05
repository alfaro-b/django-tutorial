from multiprocessing import context

from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class AllQuestionsView(generic.ListView):
    model = Question
    template_name = "polls/all.html"
    context_object_name = "all_questions"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        # Récupère le contexte initial de la vue
        context = super().get_context_data(**kwargs)

        # Ajoute les résultats du sondage au contexte
        context["choices_frequency"] = self.object.get_choices()

        return context


class StatisticsView(generic.TemplateView):
    template_name = "polls/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Nombre total de sondages
        context["total_questions"] = Question.objects.count()

        # Nombre total de choix
        context["total_choices"] = Choice.objects.count()

        # Nombre total de votes
        resultat = Choice.objects.aggregate(total=Sum('votes'))
        context['total_votes'] = resultat['total']

        # Moyenne du nombre de votes par sondage
        context['moyenne_votes_sondage'] = context["total_votes"] / context["total_questions"]

        return context
