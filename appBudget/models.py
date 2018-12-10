from django.contrib.auth.models import User
from django.db import models

"""
This model manages a category namer based on their name and description
Attributes: "max_length" = to define the maximum number of chars that the field can have
Atributes: "verbose_name" = to define the name with which it will be displayed  

"""
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    description = models.TextField(max_length=500, verbose_name='Description')

    def __str__(self):
        return self.name


"""
This model manages the budget plans of a user in a range of dates
Attributes: "on_delete" = To define the behavior of the foreign key when a planning is deleted. 
Atributes: "default" = To define the default value this field must have in case of being empty. 
"""
class Planning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='User')  # Cascade: if the parent is deleted the child is deleted
    budget = models.FloatField(default=0, verbose_name='Budget')
    date_start = models.DateField(verbose_name='Start date')
    date_end = models.DateField(verbose_name='End date')

    def __str__(self):  # To create a custom print behavior
        return '%s - %s' % (self.user, self.budget)  # user y budget


"""
This model manages the budget plannings of a user for all the categories belonging to a planning. Home › Appbudget › Category plannings › 10.0 - Home Expenses. 
Si quiero editar un valor que estaba inputed en una categoria. 
"""
class CategoryPlanning(models.Model):
    budget = models.FloatField(default=0, verbose_name='Budget')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    planning = models.ForeignKey(Planning, on_delete=models.CASCADE, verbose_name='Planning')

    def __str__(self):
        return '%s - %s' % (self.budget, self.category)


"""
This model managaes the corresponding expenses to a specific budget in the category plannings.

"""
class PlanningExpenses(models.Model):
    amount = models.FloatField(default=0, verbose_name='Amount')
    category_planning = models.ForeignKey(CategoryPlanning, on_delete=models.CASCADE, verbose_name='Category Planning')
    date = models.DateField(verbose_name='Date')
    description = models.TextField(max_length=500, verbose_name='Description')

    def __str__(self):
        return '%s - %s - %s' % (self.category_planning.category, self.amount, self.date)
        # %s reemplazo de variables la s indica que son de tipo string (seran reemplazadas por self.category_planning.category, self.amount, self.date
