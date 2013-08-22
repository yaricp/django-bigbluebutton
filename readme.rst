====================
django-bigbluebutton
====================
:Info: A Django project for interacting with BigBlueButton
:Author: Steve Challis (http://schallis.com)
	Yaric Pisarev (yaricp@gmail.com)
:Requires: BigBlueButton >= 0.71, Django >= 1.0

This is a simple Django project and application that interacts with the
`BigBlueButton <http://bigbluebutton.org>`_ API to allow you to create and
interact with web conference meetings  It currently supports:

* Password protected administration
* Meeting creation/ending
* Meeting joining
* List all currently running meetings
* User of django-portal can create own meetings
* Shedule and manage meeting for current user
* There is capability to share meeting out from the lan of firm or make closed meeting
* Manage records(create, edit share, delete) for each meeting
* Show records of meeting


Setup
=====
You'll first need to edit settings.py in the bbb_django project or your own
project. The following custom variables must be added/set in bbb/settings.py:

* SALT = "[your_salt]"
* BBB_API_URL = "http://yourdomain.com/bigbluebutton/api/"
* MAX_PARTICIPANTS = 20
* INDOOR_LANS = [list of your lans, format '192.168.100.0/24' ]
* FACILITY = "My Firm"

The `bbb` application is where all the controllers and views are contained so
you should be able to drop this into any Django project.

You can quickly test the project with the Django default webserver but you'll
probably want to have it running permenantly. `Gunicorn
<http://http://gunicorn.org/>`_ has already been added in as a dependancy so
you should be able to use `gunicorn_django` once gunicorn is installed.

It is assumed you are using FreeSWITCH for the voice calling but it is easy
enough to change the extension to that required by Asterisk.

Screenshots
===========
.. image:: https://github.com/schallis/django-bigbluebutton/raw/master/screenshots/screenshot-create.png

.. image:: https://github.com/schallis/django-bigbluebutton/raw/master/screenshots/screenshot-meetings.png
