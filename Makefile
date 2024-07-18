dev:
	poetry run flask --app weather.app run --debug

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:8000 weather:app
