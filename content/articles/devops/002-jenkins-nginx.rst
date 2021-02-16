Jenkins meet Nginx
==================

:date: 2021-02-16 20:15
:tags: jenkins, devops, server, linux, nginx
:summary: Just a quick Nginx setup for Jenkins

For a long time I run my Jenkins server only in my local Network. Therefore I
don't setup a real web server. But if I want to have some nice shields with
build status and code coverage, I need to make my Jenkins server public. And for
this, I setup Nginx as a reverse proxy. To make It secure, I enable SSL with the
certbot for Let's Encrypt. What wars rally easy.

The official documentation is quite good,
`check them out <https://www.jenkins.io/doc/book/system-administration/reverse-proxy-configuration-nginx/>`__.
If you go through my how to you have to change some values, like your domain. I
think this is all you have to change. And of course you have to set up your
domains and configure your router.

Let us started. First install Nginx and certbot

.. code-block:: bash

  sudo apt-get install -y nginx certbot python3-certbot-nginx

Then delete Nginx default site

.. code-block:: bash

  sudo rm /etc/nginx/sites-enabled/*

and also create the log directory

.. code-block:: bash

  sudo mkdir /var/log/nginx/jenkins/

Now we create the Jenkins configuration for Nginx. Create the file

.. code-block:: bash

  sudo nano /etc/nginx/sites-available/jenkins

with

.. code-block:: nginx

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  server {
    listen 80;
    server_name jenkins.example.com;

    root /var/run/jenkins/war/;
    access_log /var/log/nginx/jenkins/access.log;
    error_log /var/log/nginx/jenkins/error.log;

    location / {
      include /etc/nginx/proxy_params;

      proxy_pass         http://localhost:8080;
      proxy_read_timeout 90s;
      proxy_redirect     default;
      proxy_http_version 1.1;

      proxy_set_header   Connection        $connection_upgrade;
      proxy_set_header   Upgrade           $http_upgrade;
    }
  }

Now enable the site and restart Nginx

.. code-block:: bash

  sudo ln -s /etc/nginx/sites-available/jenkins /etc/nginx/sites-enabled/
  sudo systemctl restart nginx

If something went wrong, you can check the configuration with

.. code-block:: bash

  sudo nginx -t

The Jenkins server is now available
`jenkins.example.com <http://jenkins.example.com>`__ Change the Jenkins server
configuration so that the server only listen on the loclahost. Edit the file
*/etc/default/jenkins*

.. code-block:: bash

  sudo nano /etc/default/jenkins

Find then *JENKINS_ARGS* and add *--httpListenAddress=127.0.0.1*

.. code-block:: file

  ...
  JENKINS_ARGS="--webroot=/var/cache/$NAME/war --httpPort=$HTTP_PORT --httpListenAddress=127.0.0.1"


and restart Jenkins

.. code-block:: file

  sudo systemctl restart jenkins

SSL with Let's Encrypt
----------------------
This really easy. Simple run this

.. code-block:: bash

  sudo certbot --nginx -d jenkins.example.com

and you are done. This will also add a cron job that will update the certificate
if it expires within 30 days.
