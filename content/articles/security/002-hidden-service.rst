Hidden Service
==============

:date: 2021-02-26 20:15
:tags: security, linux, darknet, tor
:summary: Setup a hidden service on the darknet

I want to know how to set up a hidden service on the Tor network aka the
darknet. The goal is to have a copy of this blog on the darknet. Check out the
`Tor project <https://www.torproject.org>`_ to learn more about the darknet. I
will only explain how to setup a hidden servers, not the darknet himself.

**Tor project:** *We believe everyone should be able to explore the internet with
privacy. We are the Tor Project, a 501(c)3 US nonprofit. We advance human rights
and defend your privacy online through free software and open networks.*
`Meet our team. <https://www.torproject.org/about/people/>`_

Now that you know what the Tor project is, you already have the
`Tor browser <https://www.torproject.org/download/>`_ and can now read
`my blog on the darknet <http://z3wkaghfy4cmuqcrgskpvdava55qsbfrz5vvqthuemv2cktuwxvztcyd.onion/>`_,
great. But how do I create the hidden service for my blog? That was surprisingly
easy. It only takes a few steps. The
`official documentation <https://community.torproject.org/onion-services/setup/>`_
is quite well, read it and have some fun. It wars so simple that I also want to
create an example Django project behind a hidden service. Witch is just an
example and should work with all WSGI apps.

Install tor
-----------
.. code-block:: bash

  sudo apt-get install tor

You can check if the service is running

.. code-block:: bash

  sudo systemctl status tor.service
  sudo systemctl status tor@default.service

Nginx
-----
I built this blog with Pelican, a static page generator. Therefore, Nginx should
only provide some static http files.

First install Nginx

.. code-block:: bash

  sudo apt install nginx

Then delete Nginx default site

.. code-block:: bash

  sudo rm /etc/nginx/sites-enabled/*

create the server file for my blog

.. code-block:: bash

  sudo nano /etc/nginx/sites-available/axju

with

.. code-block:: nginx

  server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www/axju;
    index index.html;
    location / {
      try_files $uri $uri/ =404;
    }
  }

Create the www folder for the html files

.. code-block:: nginx

  mkdir /var/www/axju

I copied my files into this folder. Now enable the site and restart Nginx

.. code-block:: bash

  sudo ln -s /etc/nginx/sites-available/axju /etc/nginx/sites-enabled/
  sudo systemctl restart nginx

Config Tor
----------
Create folder for the Tor service

.. code-block:: bash

  sudo mkdir /var/lib/tor/axju/
  sudo chmod 700 /var/lib/tor/axju

This folder will later contain some important files for your service, like the
hostname or the private key. Now open the configuration

.. code-block:: bash

  sudo nano /etc/tor/torrc

and add this two lines

.. code-block:: bash

  HiddenServiceDir /var/lib/tor/axju
  HiddenServicePort 80 127.0.0.1:80

Your service should be available after a restart

.. code-block:: bash

  sudo systemctl restart tor

Get the hostname with

.. code-block:: bash

  sudo cat /var/lib/tor/axju/hostname


Extra - bind a WSGI app
-----------------------
It was so simple that I need something challenging. I'm going to show you how to
set up a Django project behind a hidden service. You should already know Django.

1. Setup Django
~~~~~~~~~~~~~~~
Install requirements

.. code-block:: bash

  sudo apt install python3-pip python3-venv

Create a new folder

.. code-block:: bash

  mkdir myproject
  cd myproject

Set up a new Django project with a virtual environment

.. code-block:: bash

  python3 -m venv venv
  source venv/bin/activate
  pip install django gunicorn
  django-admin startproject myproject .

Change the project settings just a bit

.. code-block:: bash

  nano myproject/settings.py

Change only the line with the allowed hosts

.. code-block:: bash

  ALLOWED_HOSTS = ['*']

2. Change the Tor config
~~~~~~~~~~~~~~~~~~~~~~~~
Open the file

.. code-block:: bash

  sudo nano /etc/tor/torrc

and change the hidden service port from

.. code-block:: bash

  ...
  HiddenServicePort 80 127.0.0.1:80

to

.. code-block:: bash

  ...
  HiddenServicePort 80 127.0.0.1:8000

Restart Tor

.. code-block:: bash

  sudo systemctl restart tor

Run gunicorn
~~~~~~~~~~~~
Run gunicorn to bind the WSGI app

.. code-block:: bash

  gunicorn --bind 127.0.0.1:8000 myproject.wsgi

Of course this is just an example. If you are setup a real service, you will use
a systemd service or something similar.


Final notes
-----------
Yes that wars easy and yes you have to do more to hide your service.

  * `Onion services best practices <https://riseup.net/en/security/network-security/tor/onionservices-best-practices>`_ by Riseup Collective
  * `Operational Security <https://community.torproject.org/onion-services/advanced/opsec/>`_

I also setup Jenkins to automate the publishing. The darknet copy of this blog
will always be a little bit newer than the main build. Uses the tor browser to
be the first one to read my post.
