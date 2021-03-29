importlib.metadata
==================
:date: 2021-03-31 20:15
:tags: python
:summary: You can write nice plugins with the entry_points section, but make sure you're not using old stuff like me.

Module **importlib.metadata** has been around since Python version 3.8. And that make **pkg_resources** some kind of deprecated.
I personally uses **pkg_resources** on two places.

1. To load some entry point, if I build a pluggable package.
2. Get the version number at runtime, if I uses setuptools-scm.

Maybe in different places, but these two pop up in my head first.
There is also a package that supplies backports of functionality for Python version smaller then 3.8
https://pypi.org/project/importlib-metadata/

Load entry points
-----------------
The Python setup script provides entry points where objects can be assigned.
In your main package, you can search for specific entry points and load them.
Other package can also defined this entry point, so your main package will load them too.
If you are interesting, I make a small video. Unfortunately, this video uses the old **pkg_resources** module.

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

Retrieving package version at runtime
-------------------------------------
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

I like this so much, that I have make this video. Unfortunately, after the video was published, I found that **pkg_resources** is some kind of deprecated.

A few days ago I published a video explaining my plugin system for Python packages.
https://youtu.be/Po5JaNVgo-M
I discovered this technique a bunch of years ago. I read Amir Rachum's Blog, how explained this technique with a funny Snek, Inc.
https://amir.rachum.com/blog/2017/07/28/python-entry-points/
Check it out my video or read the blog post for more information.

https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
https://docs.python.org/3/library/importlib.metadata.html


https://github.com/python/cpython/blob/3.9/Lib/importlib/metadata.py
https://github.com/pypa/setuptools/blob/main/pkg_resources/__init__.py
