# Yaari

A social networking platform

## Getting Started

To start working on this project, You need to make sure you have docker installed on your system and is up and running.

1. Clone the repo 
   
         git clone https://github.com/pixellateddev/yaari-backend

2. Go to project root
         
         cd yaari-backend

3. Create .env file

         touch .env

4. Add the following env variables in .env file
      
         DB_NAME=YOUR_DB_NAME
         DB_USER=YOUR_DB_USER
         DB_PASSWORD=YOUR_DB_PASSWORD

5. Build docker container

         docker-compose build

6. Initialize Django Database

         docker-compose run yaari-rest python manage.py migrate

7. Create a superuser for the application

         docker-compose run yaari-test python manage.py createsuperuser

8. Finally Run the server
         
         docker-compose up



## Built With

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)

## Contact

Himanshu Sagar - [pixellateddev@gmail.com]()