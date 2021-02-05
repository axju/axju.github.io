Jenkins meet Raspberry Pi
=========================

:date: 2021-02-06 20:15
:tags: jenkins, raspberry pi, devops, server, linux
:summary: Jenkins meet Raspberry Pi.


`pimylifeup <https://pimylifeup.com/jenkins-raspberry-pi/>`__


Setup the Raspberry Pi
----------------------
I'm using a Raspberry Pi with *Raspberry Pi OS Lite*. After writing the
operating system to the SD card, I create an empty file *SSH* in the root
directory of the SD card. This will enable the SSH server so you can simply log
in using SSH. No need to connect a keyboard or monitor. Just scan your network
with *nmap* and then connect with the default username=pi and password=raspberry.
You can also check your router to find the IP of your Raspberry Pi.

I run this

.. code-block:: bash

    nmap 192.168.178.* -p 22 --open

to find the IP. Then I connect with

.. code-block:: bash

    ssh pi@192.168.178.35

Now it's time to make your Pi just a little bit secure. We create a new user and
add them to the *sudo* group

.. code-block:: bash

  sudo adduser axju
  sudo usermod -a -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi axju

Reconnect and delete the default user *pi*

.. code-block:: bash

  exit
  ssh axju@192.168.178.35
  sudo deluser -remove-home pi

Maybe you have to kill pi's process

.. code-block:: bash

    sudo pkill -u pi

Checkout `this <https://www.raspberrypi.org/documentation/configuration/security.md>`_,
if you want to make your Raspberry Pi even more secure.

Change hostname (optional)
--------------------------
There is no need to change the name, but I like it. You can use the IP address
to connect to the server, but you can also use the hostname. So this should also
work:

.. code-block:: bash

  ssh axju@raspberrypi.local

But I will change *raspberrypi.local* to *jenkins.local*. First open the
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

Now you can connect with ``ssh axju@jenkins.local``

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

Make sure that Jenkins is running

.. code-block:: bash

  sudo systemctl status jenkins

Check the secret key

.. code-block:: bash

    sudo cat /var/lib/jenkins/secrets/initialAdminPassword

and then go to `http://jenkins.local:8080 <http://jenkins.local:8080>`__ and
enter the key. It's time to setup Jenkins. This goes straight forward. I uses
*Install suggested plugins*, see the official
`documentation <https://www.jenkins.io/doc/book/getting-started/>`__
for more information. After the plugins are installed, create a admin account.
