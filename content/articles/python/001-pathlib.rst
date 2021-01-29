Python Pathlib
==============
:date: 2021-01-29 20:15
:tags: python
:summary: I know the Pathlib is nothing new, but I only discovered in the new django default settings.

For a long time I ignore pathlib, but then came new django release with this in
the default settings.

.. code-block:: python

    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

I researched and found these links very helpful:

  * `Real Python <https://realpython.com/python-pathlib/>`_
  * `Practical Business Python <https://pbpython.com/pathlib-intro.html>`_
  * `Python Docs <https://docs.python.org/3/library/pathlib.html>`_

For more information check this out. I don't want to explain it in detail, just
give an example.

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


Example
-------
This create the folder *.axju* in your home folder and the file *data.txt* with
the content *hello*.

With **pathlib**:

.. code-block:: python

    from pathlib import Path

    data_file = Path.home() / '.axju' / 'data.txt'
    data_file.parent.mkdir(parents=True, exist_ok=True)

    with data_File.open('w') as file:
        file.write('hello')

With **os.path**:

.. code-block:: python

    import os

    home = os.path.expanduser('~')
    home_axju_dir = os.path.join(home, '.axju')
    if not os.path.exists(home_axju_dir):
        os.makedirs(home_axju_dir)

    with open(os.path.join(home_axju_dir, 'data.txt'), 'w') as file:
        file.write('hello')
