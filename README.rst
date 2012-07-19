============================
Django Fiber example project
============================

Installation:
=============

::

	$ git clone git://github.com/mvandewaeter/django-fiber-example.git
	$ cd django-fiber-example/src
	$ pip install -r requirements.txt
	$ cp settings_example.py settings.py
	$ python manage.py syncdb --migrate
	$ python manage.py loaddata ./project/fixtures/example_data/fiber.json
	$ python manage.py runserver 0:8000

::

    Or copy fiber.create.sh.example to fiber.create.sh and edit the variables inside it,
    then execute:

    $ ./fiber.create.sh
