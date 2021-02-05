Jenkins meet Nginx
==================

:status: draft
:date: 2021-02-06 20:15
:tags: jenkins, raspberry pi, devops, server, linux
:summary: ...

Install nginx and certbot for letsencrypt

.. code-block:: bash

  sudo apt-get install -y nginx certbot

Delete the default settings and creat log directory

.. code-block:: bash

  sudo rm /etc/nginx/sites-enabled/*
  sudo mkdir /var/log/nginx/jenkins/

Create a new file

.. code-block:: bash

  sudo nano /etc/nginx/sites-available/jenkins

with

.. code-block:: nginx

  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  server {
    listen 80; server_name jenkins.local;

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

  server {
    listen 443 ssl;
    server_name jenkins.axju.de;

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

Now enable the site and restart nginx

.. code-block:: bash

  sudo nginx -t
  sudo systemctl restart nginx

Change the Jenkins server configuration so that the server only listen on the
loclahost. Edit the file */etc/default/jenkins*

.. code-block:: bash

  sudo nano /etc/default/jenkins

Find then *JENKINS_ARGS* and add *--httpListenAddress=127.0.0.1*

.. code-block:: file

  ...
  JENKINS_ARGS="--webroot=/var/cache/$NAME/war --httpPort=$HTTP_PORT --httpListenAddress=127.0.0.1"


Restart Jenkins

.. code-block:: file

  sudo systemctl restart jenkins

You have to change the agent start command from

.. code-block:: file

  java -jar agent.jar -jnlpUrl http://jenkins.local:8080/computer/dragon/slave-agent.jnlp ...

.. code-block:: file

  java -jar agent.jar -jnlpUrl http://jenkins.local/computer/dragon/slave-agent.jnlp


SSL
---
.. code-block:: bash

  sudo apt install -y certbot python3-certbot-nginx
  sudo certbot --nginx -d jenkins.axju.de
