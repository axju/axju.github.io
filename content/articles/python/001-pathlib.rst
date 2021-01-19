Python Pathlib
==============

:date: 2021-01-22 20:15
:tags: python
:summary: I know the Pathlib is nothing new, but I only discovered in the new django default settings.

I know the Pathlib is nothing new, but I only discovered in the new django
default settings. I make some research and found this two links. For more
information check this out.

  * `Real Python <https://realpython.com/python-pathlib/>`_
  * `Practical Business Python <https://pbpython.com/pathlib-intro.html>`_

Everything is an object
-----------------------
The old days I uses the os.path module to work with paths. To check if a file
exist I run this:

.. code-block:: python

    >>> import os
    >>> path = 'pyth/to/my/file'
    >>> os.path.isfile(path)
    False

There the path is a string. With the *new* pathlib module, you can creates a
path object with some nice functions.

.. code-block:: python

    >>> import pathlib
    >>> path = pathlib.Path('path/to/my/file')
    >>> path.exists()
    False

The path object has more than just the function *exist()*. You can do everything
similar to the os.path module and more.


Examples
--------
Join
~~~~
Old:

.. code-block:: python

    data_file = os.path.join(os.getcwd(), 'data.json')

New:

.. code-block:: python

    data_file = Path('.') / 'data.json'
