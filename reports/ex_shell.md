# Exercice shell (2.2.2)

 python manage.py shell
8 objects imported automatically (use -v 2 for details).

Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

## Questions (2.2.2.2)

### Question 1 : afficher les attributs de chaque question

>>> Question.objects.all()
<QuerySet [<Question: What's up?>, <Question: Fait-il beau aujourd'hui?>, <Question: Quelle est la température extérieure?>, <Question: Quel est ton repas préféré?>, <Question: Quel moyen de transport utilises-tu?>, <Question: Quelle est ta saison préférée?>]>
>>> for question in Question.objects.all():
...     print(question.id, question.question_text, question.pub_date)
... 
1 What's up? 2026-11-03 07:56:56+00:00
2 Fait-il beau aujourd'hui? 2026-09-15 07:23:20+00:00
3 Quelle est la température extérieure? 2026-10-10 07:15:26+00:00
4 Quel est ton repas préféré? 2026-10-25 11:00:00+00:00
5 Quel moyen de transport utilises-tu? 2026-11-01 17:00:00+00:00
6 Quelle est ta saison préférée? 2026-11-03 08:21:40+00:00
>>> 

### Question 2 : ajouter un filtre sur la date de publication

>>> Question.objects.filter(pub_date__month=10)
<QuerySet [<Question: Quelle est la température extérieure?>, <Question: Quel est ton repas préféré?>]>
>>> 

>>> for question in Question.objects.filter(pub_date__month=10):
...     print(question.id, question.question_text, question.pub_date)
... 
3 Quelle est la température extérieure? 2026-10-10 07:15:26+00:00
4 Quel est ton repas préféré? 2026-10-25 11:00:00+00:00
>>> 

### Question 3 : Trouver la deuxième question et afficher les valeurs de tous ses attributs et tous les choix associés

>>> q = Question.objects.get(pk=2)
>>> print(q.id, q.question_text, q.pub_date)    
2 Fait-il beau aujourd'hui? 2026-09-15 07:23:20+00:00
>>> for choice in q.choice_set.all():
...     print("Choix :", choice.id, choice.choice_text, "Nbr votes:", choice.votes, "Id question:", choice.question_id)
... 
Choix : 4 Oui Nbr votes: 0 Id question: 2
Choix : 5 Non Nbr votes: 0 Id question: 2
Choix : 6 Un peu Nbr votes: 0 Id question: 2
>>> 

### Question 4 : Faire une boucle pour afficher les attributs de chaque question et leurs choix associés

>>> for question in Question.objects.all():
...     print(question.id, question.question_text, question.pub_date)    
...     for choice in question.choice_set.all():
...             print(choice.choice_text)
... 
1 What's up? 2026-11-03 07:56:56+00:00
Not much
The sky
2 Fait-il beau aujourd'hui? 2026-09-15 07:23:20+00:00
Oui
Non
Un peu
3 Quelle est la température extérieure? 2026-10-10 07:15:26+00:00
Moins de 10°
Entre 10° et 20°
Plus de 20°
4 Quel est ton repas préféré? 2026-10-25 11:00:00+00:00
Pizza
Burger
Salade
5 Quel moyen de transport utilises-tu? 2026-11-01 17:00:00+00:00
Bus
Vélo
Voiture
6 Quelle est ta saison préférée? 2026-11-03 08:21:40+00:00
Eté
Printemps
Hiver
>>> 

### Question 5 : Afficher nombre de choix enregistrés pour chaque question

>>> for question in Question.objects.all():
...     print(question.question_text, ":", question.choice_set.count(), "choix")
... 
What's up? : 2 choix
Fait-il beau aujourd'hui? : 3 choix
Quelle est la température extérieure? : 3 choix
Quel est ton repas préféré? : 3 choix
Quel moyen de transport utilises-tu? : 3 choix
Quelle est ta saison préférée? : 3 choix
>>> 

### Question 6 : optionnel

### Question 7 : Trier les questions par ordre antéchronologique

>>> for question in Question.objects.order_by("-pub_date"):
...     print(question.id, question.question_text, question.pub_date)
... 
6 Quelle est ta saison préférée? 2026-11-03 08:21:40+00:00
1 What's up? 2026-11-03 07:56:56+00:00
5 Quel moyen de transport utilises-tu? 2026-11-01 17:00:00+00:00
4 Quel est ton repas préféré? 2026-10-25 11:00:00+00:00
3 Quelle est la température extérieure? 2026-10-10 07:15:26+00:00
2 Fait-il beau aujourd'hui? 2026-09-15 07:23:20+00:00


### Question 8 : optionnel

### Question 9 : Créer une question en utilisant le shell

>>> from django.utils import timezone
>>> 
>>> q = Question(question_text="Aimes-tu le chocolat ?", pub_date=timezone.now())
>>> q.save()
>>> print(q.id, q.question_text, q.pub_date)
7 Aimes-tu le chocolat ? 2026-11-03 12:48:33.448284+00:00
>>> 

### Question 10 : Ajoutez 3 choix à cette question en utilisant le shell.

>>> q= Question.objects.get(pk=7)
>>> q.choice_set.create(choice_text="Beaucoup", votes=0)
<Choice: Beaucoup>
>>> q.choice_set.create(choice_text="Un peu", votes=0)
<Choice: Un peu>
>>> q.choice_set.create(choice_text="Pas du tout")
<Choice: Pas du tout>
>>> 

### Question 11 : Listez les questions publiées récemment. 

>>> for question in Question.objects.all():
...     if question.was_published_recently():
...         print(question.id, question.question_text, question.pub_date)
... 
1 What's up? 2026-11-03 07:56:56+00:00
6 Quelle est ta saison préférée? 2026-11-03 08:21:40+00:00
7 Aimes-tu le chocolat ? 2026-11-03 12:48:33.448284+00:00
>>> 

### Question 12 : optionnel
