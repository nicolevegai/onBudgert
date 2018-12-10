"""
WSGI config for onBudget project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/

The Web Server Gateway Interface (WSGI) is a simple calling convention for web servers
to forward requests to web applications or frameworks written in the Python programming language.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onBudget.settings')

application = get_wsgi_application()
