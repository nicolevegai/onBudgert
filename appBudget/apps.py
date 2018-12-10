"""
It is important to understand that a Django application is just a set of code that interacts with various parts of the framework.
There’s no such thing as an Application object.
However, there’s a few places where Django needs to interact with installed applications, mainly for configuration and also for introspection.
That’s why the application registry maintains metadata in an AppConfig instance for each installed application.
If you’re creating a pluggable app called “Rock ’n’ roll”, here’s how you would provide a proper name for the admin:

# rock_n_roll/apps.py

from django.apps import AppConfig

class RockNRollConfig(AppConfig):
    name = 'rock_n_roll'

"""

from django.apps import AppConfig


class AppbudgetConfig(AppConfig):
    name = 'appBudget'
