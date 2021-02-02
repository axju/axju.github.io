DevOps for blogging
===================
:status: draft
:date: 2021-02-06 20:15
:category: devops, raspberry pi
:tags: python, pelican, jenkins, raspberry pi
:summary: One easy way to automate your blogging with pelican and jenkins.


`pimylifeup <https://pimylifeup.com/jenkins-raspberry-pi/>`__


First, you'll need a small server to run Jenkins. I uses a Raspberry Pi.
Checkout `this <{filename}/articles/002-raspberry-pi-tips.rst>`__
for a minimal setup.

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

and then go to *http://jenkins-ip:8080* and enter the key. It's time to setup
Jenkins. This goes straight forward. I uses *Install suggested plugins*, see the
official `documentation <https://www.jenkins.io/doc/book/getting-started/>`__
for more informations.
