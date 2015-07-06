# goodnight-lead project

Authors: Eric Horton, Sam Magura

## Development environment setup

To install necessary Python packages:
$ sudo pip3 install -r requirements.txt

goodnight-lead uses Postgres for its database. For development, your Postgres
instance needs to have a role named "gl_dev" with password "pw" and a
database named "goodnight_lead". gl_dev needs to have CREATEDB permission for testing to work.

To run in debug mode for development, add the following to ~/.bash_profile:
    export GOODNIGHT_LEAD_DEBUG=1
    export GOODNIGHT_LEAD_TEMPLATE_DEBUG=1

To run the development server:
$ python3 manage.py runserver

Collecting staticfiles (automatically done in prod, i.e. debug = False):
$ python3 manage.py collectstatic --noinput


## Database migrations

Database backups:
https://devcenter.heroku.com/articles/heroku-postgres-backups

Migrating Databases with Django 1.8:
$ python3 manage.py makemigrations gl_site -n migrationName
$ python3 manage.py migrate gl_site xxxx_migrationName

Running migrations through Heroku:
$ heroku run python3 manage.py migrate gl_site xxxx_migrationName --app appName

## Testing

To run unit tests:
$ coverage run --source='.' manage.py test gl_site

If tests fail because static files (e.g. css, JS) can't be found, run
`manage.py collectstatic` and try again.

Generating test coverage reports:
$ coverage report
or
$ coverage html && open htmlcov/index.html


## Heroku and git

Adding a Heroku app as a git remote:
$ heroku git:remote -a appName -r remoteName

Specifying which app to use with heroku commands:
$ Add --app goodnight_lead or --app leadlabdemo

Pushing a specific branch to heroku:
$ git push -f appName branchName:master
