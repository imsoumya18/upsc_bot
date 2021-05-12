idm
==================

Downloader with Internet Download Manager (Windows)


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install idm

idm supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple idm program:

.. code-block:: python

    from idm import IDMan
    
    downloader = IDMan()
    url = "http://test.com/test.exe"
    
    downloader.download(url, r"c:\DOWNLOADS", output=None, referrer=None, cookie=None, postData=None, user=None, password=None, confirm = False, lflag = None, clip=False)


And will open "Internet Download Manager (IDM)"

or run on terminal 

.. code-block:: batch

    $ python idm.py "http://test.com/test.exe" -p C:\DOWNLOADS -o test_output.exe 

Support
------

*   Python 2.7 +, Python 3.x
*   Windows (only), for Linux you cant use wget (pip install pywget)

Links
-----

*   License: `BSD <https://bitbucket.org/licface/idm/src/default/LICENSE.rst>`_
*   Code: https://bitbucket.org/licface/idm
*   Issue tracker: https://bitbucket.org/licface/idm/issues