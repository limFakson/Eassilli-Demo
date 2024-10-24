#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess, shlex


def main():
    """Run administrative tasks."""

    """
    Running command to run faat api cli command
    """
    if "runserver" in sys.argv and not os.getenv("RUN_MAIN"):
        fastapi()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def fastapi():
    """Command for fastapi cli new view"""
    command = input("Enter command: ")
    try:
        args = shlex.split(command)

        if sys.platform == "win32":
            subprocess.Popen(["start"] + args, shell=True)
        else:
            subprocess.Popen(["gnome-terminal", "--"] + args)
    except Exception as e:
        print(f"Error occurred running FastAPI app: {e}")


if __name__ == "__main__":
    main()
