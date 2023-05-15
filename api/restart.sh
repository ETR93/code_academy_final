#!/bin/bash
PATH+=:/c/Users/Ernestas/AppData/Local/Programs/Python/Python38/python
#current_date_time=$(date)
#echo Current Date and Time is: `date +"%T"`
#echo "Current date and time: $current_date_time"

while true; do
  echo "Re-starting Django runserver"
  python manage.py runserver
  sleep 5
done