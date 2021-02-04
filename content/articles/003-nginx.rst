Some Nginx stuff
================

:status: draft

:date: 2021-02-05 2015
:tags: raspberry pi, ssh, server
:category: raspberry pi
:authors: axju
:summary: ...

.. code-block:: bash

  sudo nano /etc/nginx/sites-available/block

.. code-block:: nginx

  server {
    listen      80 default_server;
    listen      [::]:80 default_server;
    server_name _;
    return      444;
  }

.. code-block:: bash

  sudo ln -s /etc/nginx/sites-available/block /etc/nginx/sites-enabled
  sudo systemctl restart nginx
