from django.forms.models import ModelForm, BaseInlineFormSet, ModelChoiceField
from django.forms.utils import ErrorList

from appBudget.models import CategoryPlanning, PlanningExpenses
from .models import Planning


class OnBudgetBaseForm(ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):

        for field in self.base_fields:
            if isinstance(self.base_fields[field], ModelChoiceField):
                self.base_fields[field].empty_label = 'Select one option'

            self.base_fields[field].widget.attrs['class'] = 'form-control'

        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)


class PlanningForm(OnBudgetBaseForm):
    class Meta:
        model = Planning
        fields = '__all__'


class CategoryPlanningForm(OnBudgetBaseForm):
    class Meta:
        model = CategoryPlanning
        fields = '__all__'


class CategoryPlanningFormSet(BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None, save_as_new=False, prefix=None, queryset=None, **kwargs):
        for field in self.form.base_fields:
            self.form.base_fields[field].widget.attrs['class'] = 'form-control'

        super().__init__(data, files, instance, save_as_new, prefix, queryset, **kwargs)


class PlanningExpensesForm(OnBudgetBaseForm):
    class Meta:
        model = PlanningExpenses
        fields = '__all__'
