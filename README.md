# Filmweb
A real movie-fan application built with Django Framework. In this project I've implemented full user authentication system and many subdomains:

Home:
- at this page user can see upcoming movies in next 30 days in Polish cinemas, which are scraped through bs4 library. 

Films:
- at this page user can see table with all films in db and make CRUD operations on them.
- this page use pagination.
- at this page user can click on any movie and if is authenticated user can make review and rate movie.

Actors:
- at this page user can see table with all actors in db and make CRUD operations on them.
- this page use pagination.
 
Roles:
- at this page user can add role to specific actor.
 
MyProfile:
- at this page user can see a list of watched movies and list of user movie's reviews.

## General Info
A complete blogging application with post list, comments, tags and user authentication.

## Technologies:
- Python
- Django
- HTML
- CSS

## Setup

First you should clone this repository:
```
git clone https://github.com/mateuszone/Filweb.git
cd  Filmweb
```

To run the project you should have Python 3 installed on your computer. Then it's recommended to create a virtual environment for your projects dependencies. To install virtual environment:
```
pip install virtualenv
```
Then run the following command in the project directory:
```
virtualenv venv
```
That will create a new folder venv in your project directory. Next activate virtual environment:
```
source venv/bin/active
```
Then install the project dependencies:
```
pip install -r requirements.txt
```
Now you can run the project with this command:
```
python manage.py runserver
```

**Note** in the settings file you should complete your own database settings.

## Source

This is my first own project from scratch.
