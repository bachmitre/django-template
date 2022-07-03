# Django template for quick prototyping

A template for a simple bare-bone django app for quick prototyping and data modeling.

#### Running the app in development mode

Make sure that in the `docker-compose.yml` file the web container has the environment variable `ENV` set to `local`.
Also change the `SECRET_KEY` to a random string.

**docker-compose.yml:**
```shell
version: "3.3"

services:
  db:
    image: postgres
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - $PWD/postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: ["sh", "./scripts/init_django.sh"]
    ports:
      - "8000:8000"
      - "443:443"
    environment:
      - ENV=local
      - SECRET_KEY='xxxxxxx'
    volumes:
      - .:/app
    depends_on:
      - db
```

Then start the db and web container (in foreground):
```shell
docker-compose up
```
And access the app at http://localhost:8000

Since the web container mounts the local application as a volume, any code changes will directly take effect. 
However, after the model changes, do a ```Ctrl-C``` to stop the running containers, then restart them again. This will automatically create and apply the necessary migrations before starting the web application.

#### Running the app in production mode
Setting the `ENV` environment variable anything other than `local` will serve the app via ssl by gunicorn (this requires a valid cert with private key at the application root directory). 

**scripts/init_django.sh**:
```shell
...

if [ "$ENV" = "local" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    python manage.py collectstatic --noinput
    cd /app
    exec gunicorn core.wsgi:application \
        --name webserver \
        --bind 0.0.0.0:443 \
        --workers 10 \
        --log-level=info \
        --certfile=cert.pem \
        --keyfile=privkey.pem
fi
```
Then start the app via
```shell
docker-compose up
```
and access it via https://[your-cert-matching-dns-entry-pointing-to-your-machine]/ 

#### Directory structure
```shell
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── apps.py
│   ├── templates
│   │   ├── app
│   │   │   ├── base.html
│   │   │   └── index.html
│   │   └── registration
│   │       ├── base.html
│   │       ├── logged_out.html
│   │       └── login.html
│   ├── urls.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── scripts
    ├── init_db.py
    └── init_django.sh
```
