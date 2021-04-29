importlib.metadata
==================
:date: 2021-04-26 20:15
:tags: python
:summary: I didn't notice that pkg_resources was replaced by importlib.metadata from the standard library

Module `importlib.metadata <https://docs.python.org/3/library/importlib.metadata.html>`__ has been around since Python version 3.8. And that make **pkg_resources** some kind of deprecated.
I personally uses **pkg_resources** on two places and didn't realize that it was out of date.


1. To load some entry point, if I build a pluggable package.
2. Get the version number at runtime, if I uses setuptools-scm.

Maybe in different places, but these two pop up in my head first.
There is also a `package <https://pypi.org/project/importlib-metadata/>`__ that supplies backports of functionality for Python version smaller then 3.8



Load entry points
-----------------
The Python setup script provides entry points where objects can be assigned.
In your main package, you can search for specific entry points and load them.
Other package can also defined this entry point, so your main package will load them too.
If you are interesting, I make a `small video <https://youtu.be/Po5JaNVgo-M>`__. Unfortunately, this video uses the old **pkg_resources** module.

With **importlib.metadata**, the new one:

.. code-block:: python

    >>> from importlib.metadata import entry_points
    >>> for enp in entry_points()['axju.commands']:
    ...   print(enp.name)
    ...
    django
    info
    show

The old one with **pkg_resources**:

.. code-block:: python

    >>> from pkg_resources import iter_entry_points
    >>> for enp in iter_entry_points(group='axju.commands'):
    ...   print(enp.name)
    ...
    django
    info
    show

Retrieving package version at run time
--------------------------------------
You can find this example on the readme file from **setuptools-scm**.

This is how you should do it, with **importlib.metadata**:

.. code-block:: python

    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("package-name")
    except PackageNotFoundError:
        __version__ = 'Unknown'

And you'd better avoid that:

.. code-block:: python

    from pkg_resources import get_distribution, DistributionNotFound

    try:
        __version__ = get_distribution("package-name").version
    except DistributionNotFound:
        __version__ = 'Unknown'

However, this does place a runtime dependency on **setuptools** and can add up
to a few 100ms overhead for the package import time.

Conclusion
----------
As you can see, these are not major changes to the source code.
So the problem are not the adjustments, but the fact you should read the release note.
Shame on me, I don't read them very often. I only came across this while researching for my video. But even then I did get it after the video it was published.

The biggest source for my video was the `post <https://amir.rachum.com/blog/2017/07/28/python-entry-points/>`__ from Amir Rachum's Blog, which was written before the release of version 3.8. That's why he still used **pkg_resources**.


Memo to myself, read the release note
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
