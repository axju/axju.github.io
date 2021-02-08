Jenkins node
============

:status: draft
:date: 2021-02-06 20:15
:tags: jenkins, raspberry pi, devops, server, linux
:summary: ...


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
