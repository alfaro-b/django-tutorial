from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # Page de connexion gérée par Django, avec redirection vers l'accueil
    path("login/", auth_views.LoginView.as_view(template_name="polls/login.html", next_page="polls:index"), name="login"),
    path("all/", views.AllQuestionsView.as_view(), name="all"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
    path("add/", views.add, name="add"),
    path("confirm_add/", views.confirm_add, name="confirm_add"),
    # Déconnexion de l'utilisateur et retour à l'accueil
    path("logout/", auth_views.LogoutView.as_view(next_page="polls:index"), name="logout"),
]
