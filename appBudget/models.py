from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    description = models.TextField(max_length=500, verbose_name='Description')

    def __str__(self):
        return self.name


class Planning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    budget = models.FloatField(default=0, verbose_name='Budget')
    date_start = models.DateField(verbose_name='Start date')
    date_end = models.DateField(verbose_name='End date')

    def __str__(self):
        return '%s - %s' % (self.user, self.budget)


class CategoryPlanning(models.Model):
    budget = models.FloatField(default=0, verbose_name='Budget')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    planning = models.ForeignKey(Planning, on_delete=models.CASCADE, verbose_name='Planning')

    def __str__(self):
        return '%s - %s' % (self.budget, self.category)


class PlanningExpenses(models.Model):
    amount = models.FloatField(default=0, verbose_name='Amount')
    category_planning = models.ForeignKey(CategoryPlanning, on_delete=models.CASCADE, verbose_name='Category Planning')
    date = models.DateField(verbose_name='Date')
    description = models.TextField(max_length=500, verbose_name='Description')

    def __str__(self):
        return '%s - %s - %s' % (self.category_planning.category, self.amount, self.date)
