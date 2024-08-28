"""Contain apps."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """The configuration of the polls app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
