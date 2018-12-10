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
    return HttpResponse("Hello, world. You're at the polls index.")


class PlanningView(TemplateView):
    template_name = 'add_planning.html'


class PlanningListView(ListView):
    template_name = 'list_planning.html'
    queryset = Planning.objects.all()
    context_object_name = 'plannings'


class PlanningExpensesView(TemplateView):
    template_name = 'planning_expenses.html'
    user = None
    category_planning = None
    planning = None
    planning_expenses = None

    def get_context_data(self, **kwargs):
        self.user = User.objects.get(username=kwargs['username'])
        self.planning = Planning.objects.get(pk=kwargs['planning'])
        self.category_planning = CategoryPlanning.objects.filter(user=self.user, planning=self.planning)
        self.planning_expenses = []
        for cp in self.category_planning:
            for pe in cp.planningexpenses_set.all():
                self.planning_expenses.append(pe)
        return super().get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['planning_expenses'] = self.planning_expenses
        context['user'] = self.user
        return super().render_to_response(context, **response_kwargs)


class PlanningFormView(FormView):
    template_name = 'add_planning.html'
    form_class = PlanningForm
    success_url = 'add_category_planning.html'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponseRedirect(reverse('add_category_planning', args=(instance.pk,)))

    def form_invalid(self, form):
        return super().form_invalid(form)


class CategoryPlanningFormView(FormView):
    template_name = 'add_category_planning.html'
    formset = None
    form_class = CategoryPlanningForm
    success_url = 'index.html'
    planning = None

    # el metodo "get" se usa para obtener la información del contexto y mostrarla en
    # la pantalla.
    def get(self, request, *args, **kwargs):
        category_planning_formset = inlineformset_factory(Planning, CategoryPlanning, exclude=('planning', 'user',),
                                                          can_delete=False, extra=7,
                                                          formset=CategoryPlanningFormSet)
        self.planning = Planning.objects.get(pk=kwargs['pk'])
        self.formset = category_planning_formset(instance=self.planning)
        return super().get(request, *args, **kwargs)

    # El metodo "post" sirve para guardar la información de los formularios de pantalla
    def post(self, request, *args, **kwargs):
        category_planning_formset = inlineformset_factory(Planning, CategoryPlanning, exclude=('planning', 'user',),
                                                          can_delete=False, extra=7,
                                                          formset=CategoryPlanningFormSet)
        self.planning = Planning.objects.get(pk=kwargs['pk'])
        formset_post = category_planning_formset(request.POST)
        instances = formset_post.save(commit=False)
        for instance in instances:
            instance.planning = self.planning
            instance.user = self.planning.user
            instance.save()
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('list_planning'))

    def render_to_response(self, context, **response_kwargs):
        context['formset'] = self.formset
        context['planning'] = self.planning
        return super().render_to_response(context, **response_kwargs)


class PlanningExpensesFormView(FormView):
    template_name = 'add_planning_expenses.html'
    form_class = PlanningExpensesForm

    def get_context_data(self, **kwargs):
        self.form_class.base_fields['category_planning'].queryset = CategoryPlanning.objects.filter(
            user=User.objects.get(username=self.kwargs['username']))
        return super().get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['plan'] = Planning.objects.get(pk=self.kwargs['planning'])
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('list_planning'))
