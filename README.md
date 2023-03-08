# Web-App-Ride-Sharing-Service
### Run
```
cd docker-delpoy
sudo docker-compose up
```
you may also need to do
```
chmod o+x docker-deploy/web-app/initserver.sh
chmod o+x docker-deploy/web-app/runserver.sh
chmod o+x docker-deploy/web-app/startserver.sh
```
### Hierarchy
```
docker-deploy
│
├── docker-compose.yml
│
├── web-app/
│   ├── Dockerfile
│   ├── initserver.sh
│   ├── runserver.sh
│   ├── startserver.sh
│   ├── requirements.txt
│   │
│   ├── manage.py
│   ├── naive_uber/
│   │    ├── urls.py
│   │    ├── settings.py
│   │    ├── asgi.py
│   │    ├── wsgi.py
│   │    └── __init__.py
│   │
│   └── basic/
│        ├── migrations/
│        ├── static/
│        ├── templates/
│        │
│        ├── urls.py
│        ├── views.py
│        ├── models.py
│        ├── forms.py
│        ├── apps.py
│        ├── admin.py
│        ├── tests.py
│        └── __init__.py
│   
└── nginx/config/

```
