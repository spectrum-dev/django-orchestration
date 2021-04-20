## Environment Setup

# Running the Project
1. I personally have opted to use pyenv to set up my local python environment.
    a. To install pyenv, please follow the instructions [here](https://akrabat.com/creating-virtual-environments-with-pyenv/)
    b. To create a virtualenv, please run `pyenv virtualenv 3.9.0 spectrum-orchestration`
    c. To activate the virtualenv, please run `pyenv activate spectrum-orchestration`
2. To install the dependencies required for this project (like Django), run `pip install -r requirements.txt`
3. To run the Django app, please run `python manage.py runserver`

# Running Migrations
 - To run a migration, please use the command `python manage.py migrate`. Please note that the SQLite Database provided has already been configured as part of the project, so no additional setup should be needed there.
 - To revert the migrations, please use the command `python manage.py migrate orchestration zero`

# Accessing the Admin Dashboard
Django natively ships an admin dashboard that exposes a simple interface for viewing data in the application. To get this set up:

1. Create a superuser on the app by running `python manage.py createsuperuser`.
2. Fill out the username, email address and password fields that appear in the interactive interface. At the end of this flow, you should be prompted with a successful message. If any errors occur, please restart this flow and try again
3. Now, run the server (`python manage.py runserver`) and access the `http://127.0.0.1/admin` interface, input the username and password you had just created and you should enter the interface.
4. You should now see the interface with two sets of tables, one under the `API` header and the other under the `Authentication and Authorization` header. The tables under the `API` header are of concern to us for this project and reflect the models we created programatically.

# Running Tests
To run the tests, plaese run `python manage.py test`# django-orchestration
