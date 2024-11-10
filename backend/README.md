# backend

## Project setup

```sh
conda create -n backend python=3.12
conda activate backend
pip install -r requirements.txt
```

### Run migrations

```sh
python manage.py migrate
```

### Create a superuser

```sh
python manage.py createsuperuser
```

### Run the development server

```sh
python manage.py runserver
```

### Run tests

```sh
python manage.py test
```

### Format & lint

```sh
make format
make lint
```

### Run in production

```sh
export DB_NAME=app
export DB_USER=app
export DB_PASSWORD_FILE=/path/to/password/file
export DB_HOST=mysql
export DB_PORT=3306
export SECRET_KEY_FILE=/path/to/secret/key/file

export DJANGO_SETTINGS_MODULE=app.settings_prod
gunicorn -w4 -b 0.0.0.0:8000 --log-level=info app.wsgi:application
```

## Docker

See [Dockerfile](Dockerfile).
