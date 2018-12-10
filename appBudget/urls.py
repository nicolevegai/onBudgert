from django.urls import path

from appBudget.views import PlanningListView, PlanningExpensesView, PlanningFormView, CategoryPlanningFormView, \
    PlanningExpensesFormView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # create a budget planning
    path('add-planning', PlanningFormView.as_view(), name='add_planning'),

    # To add the corresponding budgets $$ to each category in a BudgetPlanning
    # The parameter  is added <pk> because it is need to identify each Budget<planning (it is the id of the previous created budget planning)
    path('add-category-planning/<pk>', CategoryPlanningFormView.as_view(), name='add_category_planning'),

    # list the existing BudgetPlannings
    path('list-planning', PlanningListView.as_view(), name='list_planning'),

    # List the expenses of the user planning
    # The parameters <planning> and <username> are added to filter the expenses for each user
    path('planning-expenses/<planning>/<username>', PlanningExpensesView.as_view(), name='planning_expenses'),

    # to Add the expenses corresponding to a user planning
    #  The parameters <planning> and <username> are added to add the corresponding expenses by planning and user
    path('add-planning-expenses/<planning>/<username>', PlanningExpensesFormView.as_view(),
         name='add_planning_expenses'),
]
