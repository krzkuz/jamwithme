release: python manage.py migrate
web: daphne jamwithme.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=jamwithme.settings -v2