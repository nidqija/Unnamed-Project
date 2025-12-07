import os
import sys
import traceback
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

def run():
    try:
        execute_from_command_line(['manage.py', 'migrate', 'items'])
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    run()
