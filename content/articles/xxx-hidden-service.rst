Hidden Service
==============

.. :status: draft

:date: 2021-02-26 20:15
:tags: security, linux, hacking, shell
:summary: Setup a hidden server for the darknet

https://community.torproject.org/onion-services/setup/
https://opensource.com/article/20/4/tor-proxy-raspberry-pi

Install tor

.. code-block:: bash

  sudo apt-get install tor

check the service

.. code-block:: bash

  sudo systemctl status tor.service
  sudo systemctl status tor@default.service

setup nginx
-----------
Install

.. code-block:: bash

  sudo apt install nginx

Then delete Nginx default site

.. code-block:: bash

  sudo rm /etc/nginx/sites-enabled/*

create config

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


create the www folder

.. code-block:: nginx

  mkdir /var/www/axju

Now enable the site and restart Nginx

.. code-block:: bash

  sudo ln -s /etc/nginx/sites-available/axju /etc/nginx/sites-enabled/
  sudo systemctl restart nginx

backup the settings

.. code-block:: bash

  sudo cp /etc/tor/torrc /etc/tor/torrc.backup

create folder for tor

.. code-block:: bash

  sudo mkdir /var/lib/tor/axju/
  sudo chmod 700 /var/lib/tor/axju

edit the configuration

.. code-block:: bash

  sudo nano /etc/tor/torrc

add

.. code-block:: bash

  HiddenServiceDir /var/lib/tor/axju
  HiddenServicePort 80 127.0.0.1:80

restart tor

.. code-block:: bash

  sudo systemctl restart tor
