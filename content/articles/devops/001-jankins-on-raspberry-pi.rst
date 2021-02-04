Jenkins meet Raspberry Pi
=========================

:date: 2021-02-06 20:15
:tags: jenkins, raspberry pi, devops, server, linux
:summary: Jenkins meet Raspberry Pi.


`pimylifeup <https://pimylifeup.com/jenkins-raspberry-pi/>`__


Basic setup
-----------
I'm using a Raspberry Pi with *Raspberry Pi OS Lite*. After writing the
operating system to the SD card, I create an empty file *SSH* in the root
directory of the SD card. This will enable the SSH server so you can simply log
in using SSH.

Scan your network to find the Raspberry Pi

.. code-block:: bash

    nmap 192.168.178.* -p 22 --open

Connect with (password=raspberry)

.. code-block:: bash

    ssh pi@192.168.178.35

Create a new user, give him administrator rights and delete the default user pi

.. code-block:: bash

    sudo adduser axju
    sudo usermod -a -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi axju
    sudo su - axju
    sudo pkill -u pi
    sudo deluser -remove-home pi

Checkout `this <https://www.raspberrypi.org/documentation/configuration/security.md>`_,
if you want to make your Raspberry Pi even more secure.

Change hostname (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~
There is no need to change the name, but I like it. You can use the IP address
to connect to the server, but you can also use the hostname. So this should also
work:

.. code-block:: bash

  ssh axju@raspberrypi.local

But I will change *raspberrypi.local* to *jenkins.local*.First open the
*/etc/hosts* file and update the lines with your old hostname:

.. code-block:: bash

  sudo nano /etc/hosts

from ``raspberrypi`` to ``jenkins``. Next change the */etc/hostname*

.. code-block:: bash

  sudo echo "jenkins" | sudo tee /etc/hostname

And finally run

.. code-block:: bash

  sudo hostname jenkins

and reboot:

.. code-block:: bash

  sudo reboot

Now you can connect with:

.. code-block:: bash

  ssh axju@jenkins.local

Install Jenkins
---------------
This is really easy. First, update your system and install Java:

.. code-block:: bash

    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y openjdk-11-jdk

Check if java is installed:

.. code-block:: bash

    java --version

Now add Jenkins source to your *sources.list*:

.. code-block:: bash

    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
    sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

No errors until now, then install Jenkins:

.. code-block:: bash

    sudo apt update
    sudo apt install -y jenkins

Check the secret key

.. code-block:: bash

    sudo cat /var/lib/jenkins/secrets/initialAdminPassword

and then go to `http://jenkins.local:8080 <http://jenkins.local:8080>`__ and enter the key. It's time to setup
Jenkins. This goes straight forward. I uses *Install suggested plugins*, see the
official `documentation <https://www.jenkins.io/doc/book/getting-started/>`__
for more information. After the plugins are installed, create a admin account.

Setup a node
------------
First create the node like this:

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-001.png
  :width: 45 %
  :alt: alternate text

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-002.png
  :width: 53 %
  :alt: alternate text


If you look at the Nodes page you can see how it starts up. Since Jenkins uses
Docker, it must be installed on the client. I am using Ubuntu but, I am sure you
can easily install it on your system. First install some requirements:

.. code-block:: bash

    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common

Add Docker source to your *sources.list*:

.. code-block:: bash

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

and install Docker:

.. code-block:: bash

  sudo apt update
  sudo apt install -y docker-ce

To run Docker without sudo, add your username to the *docker* group:

.. code-block:: bash

  sudo usermod -aG docker ${USER}

You would need to log out and log back in so that your group membership is
re-evaluated. Create a work directory for Jenkins and download the agent:

.. code-block:: bash

  mkdir ~/jenkins
  cd ~/jenkins
  wget http://jenkins.local:8080/jnlpJars/agent.jar

To connected with the client, look at the node page:

.. code-block:: bash

  java -jar ~/jenkins/agent.jar -jnlpUrl http://jenkins.local:8080/computer/dragon/slave-agent.jnlp -secret a5c9ca850ea8aacbd13d15ec434c539d3d8cadb565da198ee0ced2711ff32069 -workDir "/home/axju/jenkins"

Control with systemd
~~~~~~~~~~~~~~~~~~~~
I like to automated start the node, on system boot. Create the config file

.. code-block:: bash

  sudo nano /etc/systemd/system/jenkins-agent.service

with

.. code-block:: text

  [Unit]
  Description=jenkins-agent
  After=network.target

  [Service]
  User=axju
  WorkingDirectory=/home/axju/jenkins
  ExecStart=java -jar agent.jar -jnlpUrl http://jenkins.local:8080/computer/dragon/slave-agent.jnlp -secret a5c9ca850ea8aacbd13d15ec434c539d3d8cadb565da198ee0ced2711ff32069 -workDir "/home/axju/jenkins"

  [Install]
  WantedBy=multi-user.target

Start service and enable it for automate start

.. code-block:: bash

  sudo systemctl start jenkins-agent
  sudo systemctl enable jenkins-agent

To make sure that everything works fine, run

.. code-block:: bash

  sudo systemctl status jenkins-agent

Jenkins hello world
-------------------
Make sure you have installed the *Docker plugin*. Go to
`http://jenkins.local:8080/pluginManager/installed <http://jenkins.local:8080/pluginManager/installed>`__
and search for *Docker*. If it's not available, install.

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-003.png
  :width: 100 %
  :alt: alternate text

Then create a new Pipeline Job with the name *hello-world*.

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-004.png
  :width: 49 %
  :alt: alternate text

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-005.png
  :width: 49 %
  :alt: alternate text

This simple Pipeline script uses the python docker and only print the python version.

.. code-block:: jenkins

  pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
  }

Now run you new job.

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-006.png
  :width: 33 %
  :alt: alternate text

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-007.png
  :width: 33 %
  :alt: alternate text

.. image:: {static}/images/articels/jankins-on-raspberry-pi/jenkins-008.png
  :width: 33 %
  :alt: alternate text


Did you make it this far? Congratulations, your little Jenkins server is up and
running. To be honest, it took me a while to get there

Nginx
-----
Install nginx and certbot for letsencrypt

.. code-block:: bash

  sudo apt-get install -y nginx certbot

Delete the default settings and creat log directory

.. code-block:: bash

  sudo rm /etc/nginx/sites-enabled/*
  sudo mkdir /var/log/nginx/jenkins/

Create a new file

.. code-block:: bash

  sudo nano /etc/nginx/sites-available/jenkins.local

with

.. code-block:: nginx

  upstream jenkins {
    keepalive 32; # keepalive connections
    server 127.0.0.1:8080; # jenkins ip and port
  }

  # Required for Jenkins websocket agents
  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  server {
    listen 80;
    server_name jenkins.local;

    root            /var/run/jenkins/war/;
    access_log      /var/log/nginx/jenkins/access.log;
    error_log       /var/log/nginx/jenkins/error.log;

    location / {
      sendfile off;
      proxy_pass         http://jenkins;
      proxy_redirect     default;
      proxy_http_version 1.1;

      # Required for Jenkins websocket agents
      proxy_set_header   Connection        $connection_upgrade;
      proxy_set_header   Upgrade           $http_upgrade;

      proxy_set_header   Host              $host;
      proxy_set_header   X-Real-IP         $remote_addr;
      proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto $scheme;
      proxy_max_temp_file_size 0;

      #this is the maximum upload size
      client_max_body_size       10m;
      client_body_buffer_size    128k;

      proxy_connect_timeout      90;
      proxy_send_timeout         90;
      proxy_read_timeout         90;
      proxy_buffering            off;
      proxy_request_buffering    off; # Required for HTTP CLI commands
      proxy_set_header Connection ""; # Clear for keepalive
    }
  }

Now enable the site and restart nginx

.. code-block:: bash

  sudo ln -s /etc/nginx/sites-available/jenkins.local /etc/nginx/sites-enabled
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

  sudo apt install -y nginx python-certbot-nginx
  sudo certbot --nginx -d jenkins.axju.de
