from django.shortcuts import render

from appBudget.models import Planning

"""
This python method is in charge of serving the system's main page and all the information that is needed inside it

"""

def index(request):
    planning_list = Planning.objects.all()

    return render(request, 'index.html', {
        'planning_list': planning_list
    })
