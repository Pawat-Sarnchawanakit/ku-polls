"""Entry point of the app."""
import os
import time
import socket
from decouple import config
from django.core.management import execute_from_command_line

def main():
    """The main function."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    host = None
    for i in range(0, 30):
        try:
            host = socket.gethostbyname("db")
        except:
            print(f"Wating for db hostname attempt {i}")
            time.sleep(1)
            continue
        break
    if host is None:
        print("Failed to resolve database's host")
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(0, 30):
        try:
            s.connect((host, 5432))
        except:
            print(f"Wating for db attempt {i}")
            time.sleep(1)
            continue
        break
    execute_from_command_line(("manage.py", "migrate"))
    if config('LOAD_DATA', default=False, cast=bool):
        execute_from_command_line(("manage.py", "loaddata", "data/users.json"))
        execute_from_command_line(("manage.py", "loaddata", "data/polls-v4.json"))
        execute_from_command_line(("manage.py", "loaddata", "data/votes-v4.json"))
    execute_from_command_line(("manage.py", "runserver", "0.0.0.0:8000"))

main()
