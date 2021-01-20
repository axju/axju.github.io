axju bloggin source
===================

Setup

.. code:: bash

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip pelican

Create html:

.. code:: bash

    pelican content
    pelican content -s publishconf.py

Preview your site:

.. code:: bash

    pelican --listen
