from django.urls import path

from appBudget.views import PlanningListView, PlanningExpensesView, PlanningFormView, CategoryPlanningFormView, \
    PlanningExpensesFormView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-planning', PlanningFormView.as_view(), name='add_planning'),
    path('add-category-planning/<pk>', CategoryPlanningFormView.as_view(), name='add_category_planning'),
    path('list-planning', PlanningListView.as_view(), name='list_planning'),
    path('planning-expenses/<planning>/<username>', PlanningExpensesView.as_view(), name='planning_expenses'),
    path('add-planning-expenses/<planning>/<username>', PlanningExpensesFormView.as_view(),
         name='add_planning_expenses'),
]
