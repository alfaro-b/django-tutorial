from django.db.models import Sum
from .models import Question


def minimax():
    questions = Question.objects.all()

    first_question = questions[0]
    first_total = first_question.choice_set.aggregate(total=Sum('votes'))['total'] or 0

    min = max = (first_question, first_total)

    for q in questions:
        n = q.choice_set.aggregate(sum=Sum('votes'))['sum']

        if n > max[1]:
            max = (q, n)

        if n < min[1]:
            min = (q, n)

    return (min[0], max[0])
