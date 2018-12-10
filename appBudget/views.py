from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from appBudget.forms import PlanningForm, CategoryPlanningForm, CategoryPlanningFormSet, PlanningExpensesForm
from appBudget.models import Planning, CategoryPlanning


def index(request):
    return HttpResponse("Hello. You're at the polls index.")


class PlanningView(TemplateView):
    template_name = 'add_planning.html'


"""
View to show in screen the list of existing budget Plannings 
attribute: template_name= to link with the screen that we want to see
Attribute: queryset = To obtain the filter that is going to be displayed on screen (at least the main one)
Attribute: context_object_name = to put a name to the filter of the previous parameter  (queryset) Ex: {% plannings %}
"""
class PlanningListView(ListView):
    template_name = 'list_planning.html'
    queryset = Planning.objects.all()
    context_object_name = 'plannings'


"""
View to show in screen the list of expenses in a Planning  
Attribute: user, category_planning, planning, planning_expenses = variables used inside the class
"""
class PlanningExpensesView(TemplateView):
    template_name = 'planning_expenses.html'
    user = None
    category_planning = None
    planning = None
    planning_expenses = None

    # method to get the values that come in the URL "username" and "planning" to obtain with them the lists of
    # "self.category_planning" and "self.planning_expenses" which will be displayed on screen.
    def get_context_data(self, **kwargs):
        self.user = User.objects.get(username=kwargs['username'])
        self.planning = Planning.objects.get(pk=kwargs['planning'])
        self.category_planning = CategoryPlanning.objects.filter(user=self.user, planning=self.planning)
        self.planning_expenses = []
        for cp in self.category_planning:
            for pe in cp.planningexpenses_set.all():
                self.planning_expenses.append(pe)
        return super().get_context_data(**kwargs)

    # Method to add the information that is wanted to display on screen
    def render_to_response(self, context, **response_kwargs):
        # adding the filtered expenses for a user and planning
        context['planning_expenses'] = self.planning_expenses
        context['user'] = self.user
        return super().render_to_response(context, **response_kwargs)


"""
View with the form to add a Budget Planning 
Attribute: form_class =Indicates the model in from which we want to create the form 
Attribute: success_url = Indicates the url that is wanted, once the form is correclty saved  that is where the user can record the budget planned for each categories 
"""
class PlanningFormView(FormView):
    template_name = 'add_planning.html'
    form_class = PlanningForm
    success_url = 'add_category_planning.html'

    # method to save the form once it is correct
    def form_valid(self, form):
        instance = form.save()
        return HttpResponseRedirect(reverse('add_category_planning', args=(instance.pk,)))

    def form_invalid(self, form):
        return super().form_invalid(form)


"""
View of the categories ready to get budget inputs 
"""
class CategoryPlanningFormView(FormView):
    template_name = 'add_category_planning.html'
    formset = None
    form_class = CategoryPlanningForm
    success_url = 'index.html'
    planning = None

    # the method "get" is used to obtain the information from the context and display it on screen
    def get(self, request, *args, **kwargs):
        category_planning_formset = inlineformset_factory(Planning, CategoryPlanning, exclude=('planning', 'user',),
                                                          # we exclude because we dont need that info, and we dont have a model that shows this specific needs (category and budget) so we use CategoryPlanningFormSet
                                                          formset=CategoryPlanningFormSet)
        self.planning = Planning.objects.get(pk=kwargs['pk'])  # para mostrar en el screen el username
        self.formset = category_planning_formset(instance=self.planning)
        return super().get(request, *args, **kwargs)

    # The method "post" saves the information from the forms on screen
    def post(self, request, *args, **kwargs):
        category_planning_formset = inlineformset_factory(Planning, CategoryPlanning, exclude=('planning', 'user',),
                                                          can_delete=False, extra=7,
                                                          formset=CategoryPlanningFormSet)  #es lo que tiene que guardar
        self.planning = Planning.objects.get(pk=kwargs['pk'])
        # In (request.POST) all the forms information (formset) is stored
        formset_post = category_planning_formset(request.POST)
        # A  "fake" "save" is executed to obtain the instances (objects) that were recorded on screen
        instances = formset_post.save(commit=False)

        # Iteration over the instances to add the user and the corresponding planning ya que no estaban en pantalla
        for instance in instances:
            instance.planning = self.planning
            instance.user = self.planning.user
            instance.save()
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('list_planning'))

        # method to put the neccesary variables in context ( so they can be seen in the HTML pages)
        # formset = {{ formset }}, planning = {{ planning }}
    def render_to_response(self, context, **response_kwargs):
        context['formset'] = self.formset
        context['planning'] = self.planning
        return super().render_to_response(context, **response_kwargs)


"""
View with the form to add the expenses per caategory in a Planning 
"""
class PlanningExpensesFormView(FormView):
    template_name = 'add_planning_expenses.html'
    form_class = PlanningExpensesForm

    def get_context_data(self, **kwargs):
        # filter the category_planning according to the user that is requesting for the expenses.
        # Because of this, in the dropdown only the CategoryPlanning that belong to a specific user are shown
        # (the username is obtained from the parameter in the URL)

        self.form_class.base_fields['category_planning'].queryset = CategoryPlanning.objects.filter(
            user=User.objects.get(username=self.kwargs['username']))
        return super().get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['plan'] = Planning.objects.get(pk=self.kwargs['planning'])
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        form.save()
        # redirect the flow of the system to an specific URL
        return HttpResponseRedirect(reverse('list_planning'))
