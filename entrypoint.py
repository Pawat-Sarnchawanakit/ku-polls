"""Entry point of the app."""
import os
import time
from django.core.management import execute_from_command_line

def main():
    """The main function."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    time.sleep(5)
    execute_from_command_line(("manage.py", "migrate"))
    execute_from_command_line(("manage.py", "runserver", "0.0.0.0:8000"))

main()
