#!/bin/bash
PATH+=:/c/Users/Ernestas/AppData/Local/Programs/Python/Python38/python

while true; do
  echo "Re-starting Django runserver"
  python manage.py runserver
  sleep 5
done