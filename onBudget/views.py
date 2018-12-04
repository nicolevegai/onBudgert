from django.shortcuts import render

from appBudget.models import Planning


def index(request):
    planning_list = Planning.objects.all()

    return render(request, 'index.html', {
        'planning_list': planning_list
    })
