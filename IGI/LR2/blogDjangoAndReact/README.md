# Django and React integration #

This web application consists on a basic personal blog to make posts, to create categories, this also includes featured posts shown on slider, user registration, login, comments on each post by logged in users, rate post with stars by logged in users, calculate average rating as well, and uploading content of categories and posts (text and images) using Django admin and the data is shown on a react frontend application.

## Examples (images) ##
[Demo (image 1)](https://user-images.githubusercontent.com/59356298/103450354-23347800-4c83-11eb-85d9-bdad72bfdb16.png "demo 1")  
[Demo (image 2)](https://user-images.githubusercontent.com/59356298/103450370-68f14080-4c83-11eb-968d-429126c37ee8.png "demo 2")

## Programming languages (frameworks, libraries) ##
*   Django (Django rest framework, Django models, Django admin, JSON, serialization, Simple JSON Web Token authentication)
*   Reactjs (HTML, CSS, reactstrap, react redux, react route, JSON)

## Database ##
*   MySQL

## Installation (with docker) ##
*   First of all, create a file named .env located in the directory backend_django/ and write the next credentials:
```
DEBUG=True
SECRET_KEY=django-insecure-$nbsnagx0*0w0k_7o@$rt83#3@v%7u=_iu3=y7cd_o-aanydg$
DATABASE_HOST=db
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_PORT=3306
DATABASE_NAME=posts
DATABASE_PASSWORD=root
DATABASE_USER=root
``` 
*   You can install the application with docker with just these two commands: 
	* ### `docker-compose build`
*   The command above will take a while, after that run: 
	* ### `docker-compose up -d`
*   Now the application is ready, to create a super user to save data using the django admin use the following command: 
	* ### `docker exec -it container_id python manage.py createsuperuser`
*   The frontend application will run in the next link: 
```
http://localhost:3000/
``` 
*   The admin will run in the following link: 
```
http://localhost:8000/admin
``` 
*   Now is all ready, don't use the installation and how to run it that is below: 

## Installation (without docker) ##
*   First create a MySQL database named "posts" 
*   To connect the Django application with the MySQL database, create a file named .env located in the directory backend_django and configurate the cretentials, host and so on.
```
DEBUG=True
SECRET_KEY=django-insecure-$nbsnagx0*0w0k_7o@$rt83#3@v%7u=_iu3=y7cd_o-aanydg$
DATABASE_HOST=localhost
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_PORT=3306
DATABASE_NAME=posts
DATABASE_PASSWORD=
DATABASE_USER=root
``` 
*   Create a virtual enviroment for the django dependencies [Link official documentation](https://docs.djangoproject.com/en/3.1/intro/contributing/#getting-a-copy-of-django-s-development-version "djangoenviroment")
*   Activate the enviroment and go to the backend_django folder and install the Django dependencies with the following command using the requirements.txt file which has the dependencies
	* ### `pip install -r requirements.txt`
*   To create the tables on the database, on the backend_django folder run the following commands (python or python3 depends on your configuration when the enviroment variable on the system was set up)
	* ### `python manage.py makemigrations`
	* ### `python manage.py migrate`
*   To upload the content using Django admin, a super user has to be created, see official documentation [Link official documentation Django admin](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#introducing-the-django-admin "djangoenviroment")
*   To install the react application, go to the frontend_reactjs folder and run
	* ### `yarn install`

## How to run it ##
*   Go to the backend_django folder and run
	* ### `python manage.py runserver`
*   Also go to the frontend_reactjs folder and run
	* ### `yarn start`

## Running tests ##
*   To run test for backend, go to the backend_django folder and run:
	* ### `python manage.py test posts`

## Notes ##
*   If different ports are being used, go to the settings.py file and change the port in the whitelist, or change the port in the baseUrl.js file, it depends on the configuration.
*   This application is not using https yet, it uses http, when deploying the application, I suggest using https, a private key and a public key (SSL) for exchanging data between client and server for security.

## Credits ##
*   [Tutorial django rest framework](https://bezkoder.com/django-crud-mysql-rest-framework/ "djangorestframeworktutorial")