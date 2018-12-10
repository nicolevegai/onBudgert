"""
If you’re building a database-driven app, chances are you’ll have forms that map closely to Django models.
For instance, you might have a BlogComment model, and you want to create a form that lets people submit comments.
In this case, it would be redundant to define the field types in your form, because you’ve already defined the fields in your model.

For this reason, Django provides a helper class that lets you create a Form class from a Django model

Model Choice Field
Allows the selection of a single model object, suitable for representing a foreign key.
Note that the default widget for ModelChoiceField becomes impractical when the number of entries increases.
You should avoid using it for more than 100 items.

A single argument is required:
queryset¶
A QuerySet of model objects from which the choices for the field are derived and which is used to validate the user’s selection.
It’s evaluated when the form is rendered.

Baseinlineformset
Inline formsets is a small abstraction layer on top of model formsets.
These simplify the case of working with related objects via a foreign key.
"""

from django.forms.models import ModelForm, BaseInlineFormSet, ModelChoiceField
from django.forms.utils import ErrorList

from appBudget.models import CategoryPlanning, PlanningExpenses
from .models import Planning


class OnBudgetBaseForm(ModelForm):  # sets bases
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):  #sets default values

        for field in self.base_fields:
            if isinstance(self.base_fields[field], ModelChoiceField):
                self.base_fields[field].empty_label = 'Select one option'

            self.base_fields[field].widget.attrs['class'] = 'form-control'

        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)


class PlanningForm(OnBudgetBaseForm):  #creating planning form with all fields inherited by OnBudgetBaseForm Class
    class Meta:
        model = Planning
        fields = '__all__'


class CategoryPlanningForm(
    OnBudgetBaseForm):  #creating CategoryPlanningForm with all fields inherited by OnBudgetBaseForm Class
    class Meta:
        model = CategoryPlanning
        fields = '__all__'


class CategoryPlanningFormSet(BaseInlineFormSet):  #creates a base for the category planning sets
    def __init__(self, data=None, files=None, instance=None, save_as_new=False, prefix=None, queryset=None, **kwargs):
        for field in self.form.base_fields:
            self.form.base_fields[field].widget.attrs['class'] = 'form-control'

        super().__init__(data, files, instance, save_as_new, prefix, queryset, **kwargs)


class PlanningExpensesForm(
    OnBudgetBaseForm):  #creating Planning Expenses Form with all fields inherited by OnBudgetBaseForm Class
    class Meta:
        model = PlanningExpenses
        fields = '__all__'
