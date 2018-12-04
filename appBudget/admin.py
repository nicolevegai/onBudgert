from django.contrib import admin

from .models import Category, Planning, CategoryPlanning, PlanningExpenses


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(Category, CategoryAdmin)


class PlanningAdmin(admin.ModelAdmin):
    list_display = ['display_username', 'budget', 'date_start', 'date_end']

    def display_username(self, obj):
        return obj.user.username


admin.site.register(Planning, PlanningAdmin)


class CategoryPlanningAdmin(admin.ModelAdmin):
    list_display = ['display_username', 'display_category']

    def display_username(self, obj):
        return obj.user.username

    def display_category(self, obj):
        return obj.category.name


admin.site.register(CategoryPlanning, CategoryPlanningAdmin)


class PlanningExpensesAdmin(admin.ModelAdmin):
    list_display = ['category_planning', 'date', 'description', 'amount']


admin.site.register(PlanningExpenses, PlanningExpensesAdmin)
