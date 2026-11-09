from django import forms


# Définition des champs et des règles de validation du formulaire
class QuestionForm(forms.Form):
    question_text = forms.CharField(
        label="Question",
        max_length=200
    )

    # Champs facultatifs pour les choix associés à la question
    choice_0 = forms.CharField(label="Choix 1", required=False)
    choice_1 = forms.CharField(label="Choix 2", required=False)
    choice_2 = forms.CharField(label="Choix 3", required=False)
    choice_3 = forms.CharField(label="Choix 4", required=False)
    choice_4 = forms.CharField(label="Choix 5", required=False)
    