"""
One of the most powerful parts of Django is the automatic admin interface.
It reads metadata from your models to provide a quick, model-centric interface
where trusted users can manage content on your site.
If you’re not using the default project template, here are the requirements:

1. Add 'django.contrib.admin' and its dependencies - django.contrib.auth, django.contrib.contenttypes, django.contrib.messages, and django.contrib.sessions - to your INSTALLED_APPS setting.
2. Configure a DjangoTemplates backend in your TEMPLATES setting with django.contrib.auth.context_processors.auth and django.contrib.messages.context_processors.messages in the 'context_processors' option of OPTIONS.
3. If you’ve customized the MIDDLEWARE setting, django.contrib.auth.middleware.AuthenticationMiddleware and django.contrib.messages.middleware.MessageMiddleware must be included.
If you need to create a user to login with, use the createsuperuser command. By default, logging in to the admin requires that the user has the is_superuser or is_staff attribute set to True
Finally, determine which of your application’s models should be editable in the admin interface. For each of those models, register them with the admin as described in ModelAdmin.
"""
from django.contrib import admin

# from class models import the following classes to be editable in the admin interface:
from .models import Category, Planning, CategoryPlanning, PlanningExpenses


#
class CategoryAdmin(admin.ModelAdmin):  # Categorys
    # shows all the categories available
    list_display = ['name', 'description']  # create a list where name and description of each category is shown.


admin.site.register(Category, CategoryAdmin)  #register the category in CategoryAdmin


class PlanningAdmin(admin.ModelAdmin):  # Plannings
    # all the planned budgets are displayed here
    list_display = ['display_username', 'budget', 'date_start', 'date_end']  # create a list with this elements

    def display_username(self, obj):  #needed to show the username in the list
        return obj.user.username


admin.site.register(Planning, PlanningAdmin)


class CategoryPlanningAdmin(admin.ModelAdmin):  # Category Plannings
    # done to show all the categories created for each user
    list_display = ['display_username', 'display_category']  # create a list with this elements

    def display_username(self, obj):  #needed to show the username in the list
        return obj.user.username

    def display_category(self, obj):  #needed to show the category in the list
        return obj.category.name


admin.site.register(CategoryPlanning, CategoryPlanningAdmin)


class PlanningExpensesAdmin(admin.ModelAdmin):  # Planning expenses
    # shows all the expenses
    list_display = ['category_planning', 'date', 'description', 'amount']  # create a list with this elements


admin.site.register(PlanningExpenses, PlanningExpensesAdmin)
