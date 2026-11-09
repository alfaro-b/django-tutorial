from multiprocessing import context

from django.db.models import F, Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .utils import minimax
from .forms import QuestionForm

from .models import Choice, Question

NB_MAX_CHOIX = 5


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


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

        # Questions les moins et les plus populaires
        (context["least_popular_question"], context["most_popular_question"]) = minimax()

        # Nombre de votes des questions les plus et les moins populaires
        context["most_popular_votes"] = (
                context["most_popular_question"].choice_set.aggregate(total=Sum("votes"))["total"] or 0
        )

        context["least_popular_votes"] = (
                context["least_popular_question"].choice_set.aggregate(total=Sum("votes"))["total"] or 0
        )

        # Dernière question enregistrée
        latest_question_id = Question.objects.aggregate(max=Max('id'))['max']
        context["latest_question"] = Question.objects.get(pk=latest_question_id)

        return context


def add(request):
    if request.method == "POST":
        # Formulaire lié aux données envoyées par l'utilisateur
        form = QuestionForm(request.POST)

        if form.is_valid():
            # Récupération des données validées et enregistrement de la question
            question = Question(
                question_text=form.cleaned_data["question_text"],
                pub_date=timezone.now()
            )
            question.save()

            # Enregistrement des choix jusqu'au premier champ vide
            for no_choix in range(NB_MAX_CHOIX):
                field_name = "choice_{}".format(no_choix)
                choice_text = form.cleaned_data[field_name]

                if choice_text:
                    choice = Choice(
                        question=question,
                        choice_text=choice_text
                    )
                    choice.save()
                else:
                    break

            # Redirection après l'enregistrement pour éviter un nouvel envoi
            return redirect("polls:confirm_add")

    else:
        # Création d'un formulaire vide lors d'une requête GET
        form = QuestionForm()

    # Affichage du formulaire, avec les erreurs éventuelles
    return render(request, "polls/add.html", {"form": form})


def confirm_add(request):
    return render(request, "polls/confirm_add.html")
