intrepidboats
===============

[![build status](//gitlab.devartis.com/samples/django-sample/badges/master/build.svg)](http://gitlab.devartis.com/samples/django-sample/commits/master)

## Requirements:
* Python >= 3.4 
* pip
* [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html)/[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
    - `sudo pip install virtualenvwrapper`
    - add `source /usr/local/bin/virtualenvwrapper.sh` to your shell config (.bashrs or .zshrs)
    - restart your terminal

## Local Setting's 
* copy settings/local_example.py to settings/local.py. Replace environment variables with local values.
    - `cp intrepidboats/settings/local_example.py intrepidboats/settings/local.py`
    - `cp intrepidboats/settings/.env.default_local intrepidboats/settings/.env`
    
## Local setUp
* `mkvirtualenv --python=/usr/bin/python3 intrepidboats` or `workon intrepidboats`
* `pip install -r requirements/local.txt`
* `export DJANGO_SETTINGS_MODULE=intrepidboats.settings.local`
* `./manage.py migrate`
* `./manage.py populate_home`
* `./manage.py populate_boats`
* `./manage.py populate_articles`
* `./manage.py populate_events`
* `./manage.py populate_gallery`
* `./manage.py import_all_forum_data`

## Run server
* `./manage.py runserver`

## Run Lint/Style/CPD:
* Instalar `nodejs` y [jscpd](https://github.com/kucherenko/jscpd)
* pep8: `sh scripts/pep8.sh`
* pylint: `sh scripts/pylint.sh`
* cpd: `sh scripts/jscpd.sh`


## Git hooks
* Bajar binario de [git-hooks](https://github.com/git-hooks/git-hooks/releases) y agregarlo al PATH.
* Instalar hooks: `git hooks install`


## Use postgres with docker container

* Run `docker run --name intrepidboats-postgres -e POSTGRES_PASSWORD=intrepidboats -e POSTGRES_USER=intrepidboats -e POSTGRES_DB=intrepidboats -p 5432:5432 -d postgres:9.6.1`
* Change database settings at local.py for using that port (see local_example.py)

## Pycharm IDE
* config virtualenv created before as the virtualenv of the project (settings -> python interpreter)
* enable django support: settings -> django 
    - django project root: /home/diego/dev/projects/python/intrepidboats
    - settings: intrepidboats/settings/local.py
    - manage script: manage.py
* mark directory Templates as "Templates folder" (right-click over directory in the "Project view")

## Development database population

1) Populate home page slide: `python manage.py populate_home`

