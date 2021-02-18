A reverse shell with Python
===========================

.. :status: draft

:date: 2021-02-19 20:15
:tags: python,
:summary: ...


https://www.acunetix.com/blog/web-security-zone/what-is-reverse-shell/

**Disclaimer**: The methods described only be used for systems for which you
have access rights. I used this method to get access to my mums PC, which I was
allowed. And yes, I'm 31, have my own family, but still help my mom with her PC.


First the basics. If you want to access a target, you need two programs. One on
the target waiting for the incoming connection. And one on your system to make
the connection. There are tons of programs, but really common and secure is the
Secure Shell (`SSH <https://en.wikipedia.org/wiki/SSH_(Secure_Shell)>`__). If I
configure my server I always use SSH. I don't need physical access or have to
plug a keyboard or monitor. I only need a network connection. The server runs
the ssh server program (`sshd <https://www.ssh.com/ssh/sshd/>`__) which waiting
to incoming connections. The client program connects to the server.

If you are using a revers shell, the tasks are reversed. On your client is run a
server program, which listening for incoming connections. And the target execute
a program, which connect to your client. Then you can run commands on the target
from your client.

Why you should use a reverse shell? Why not always the direct way? If your
target is behind a firewall, you can not access. If you use the direct way, your
target must be attainable. In most cases you have no influence on the target,
but on your system. That was enough information now. Use google to find more.
Now let's have fun

Python
------

Server
~~~~~~

Client
~~~~~~

Public server
-------------
