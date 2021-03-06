Raspberry Pi Tips
=================

:status: draft

:date: 2021-02-05 2015
:tags: raspberry pi, ssh, server
:category: raspberry pi
:authors: axju
:summary: Some simple tips for Raspberry Pi users.

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

Public Key
----------
Check if you have any ssh keys:

.. code-block:: bash

  ls ~/.ssh/*pub

I have the public key::

  /home/axju/.ssh/id_rsa.pub

If you don't have one, create one:

.. code-block:: bash

  ssh-keygen -b 4096

Copy public key to the server:

.. code-block:: bash

  ssh-copy-id -i ~/.ssh/id_rsa.pub axju@192.168.178.35

if *sh-copy-id* don't work use *scp*, but this will delete other authorized keys:

.. code-block:: bash

  ssh axju@192.168.178.35 "mkdir .ssh"
  scp ~/.ssh/id_rsa.pub axju@192.168.178.35:.ssh/authorized_keys
