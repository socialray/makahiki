# README.md

## Introduction

This README describes how to set up your computer for Makahiki Development.

## Prerequisites
* [Python](http://www.python.org/download/) 2.6 or higher (but not Python 3).  On Windows machines, it is recommended that you use the 32 bit version, as using the 64 bit version appears to have issues.  Verify that you have it installed by typing `python` at the command prompt.  The interpreter should launch.  Close the interpreter by typing `exit()`.
* If on Mac OS X, make sure that the Apple Developer Tools are installed (which is bundled with XCode).  You can either get this from your Mac's install DVD or from Apple's [site](http://developer.apple.com/technologies/xcode.html).  Note that you need an Apple developer account (which is free) to download from Apple.
* [Python Imaging Library](http://www.pythonware.com/products/pil/) (PIL). If you are on OSX, it is easier to install via [Homebrew](http://mxcl.github.com/homebrew/). Once Homebrew is installed, install PIL by typing `brew install pil`. If you are brave enough to install from source, make sure you have both libjpeg and zlib for jpeg and png support respectively.
* Git.  Find a package for your operating system at the [GitHub install wiki](http://help.github.com/git-installation-redirect). It is recommended that you also configure Git so that it handles line endings from Windows users correctly. See [Dealing With Line Endings](http://help.github.com/dealing-with-lineendings/).
* Pip. Check if it is installed by typing `pip help`. If not, install it by typing `easy_install pip`. If you do not have easy_install, download and follow the instructions [here](http://pypi.python.org/pypi/setuptools).
* _Optional but recommended_ [Virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/). Virtualenv and Virtualenvwrapper allow you to install libraries separately from your global Python path. Follow the steps in the introduction and make a virtualenv for Makahiki (i.e. `mkvirtualenv makahiki`). You may also want to define $WORKON_HOME to your shell startup file in addition to adding the virtualenv startup script (it uses `~/.virtualenv` by default).

## Obtaining the Makahiki source
* If you only wish to download the source, you can check out using the read-only URL.  Type `git clone git://github.com/csdl/makahiki.git` to get the source.
* If you wish to commit to the Makahiki project, you will need to create an account at [GitHub](http://github.com).  Then, you will need to set up your [SSH keys](http://help.github.com/key-setup-redirect) and your [email settings](http://help.github.com/git-email-settings/).
* Once those are set up, send me your Git username so that you can be added as a collaborator.
* When you are added as a collaborator, you should be able to check out the code by using the private url.  Type `git clone git@github.com:csdl/makahiki.git` to check out the code.  This will create the new folder and download the code from the repository.

## Grabbing External Dependencies
The following steps are to download additional libraries and upgrade some of the default ones.

* cd into the makahiki/makahiki folder.
* If you used virtualenvwrapper, start the virtual environment by typing `workon <environment-name>`.
* Type `pip install -r requirements.txt` from the application root.  This will load the dependencies in requirements.txt.

## Setting up Makahiki
* If you used virtualenvwrapper, activate the virtual environment by typing `workon <environment-name>`.
* Update makahiki_settings.py with the settings related to the competition.  Important settings include the CAS authentication server for your organization and your time zone.
* Copy example\_settings/local\_settings.py.dev to local\_settings.py.  This file provides additional modules for testing and can be used to override previously defined settings.  For example, you can specify a different database in this file.
* Type `python manage.py syncdb --noinput` to create the database.
* Run `python manage.py migrate` to sync the migrations.
* To load some sample data into the application, type `./scripts/load_data.sh`.  If you are on Windows, you can use `scripts\load_data.bat`.

## Running the server
* Type `python manage.py runserver` to start the web server.
* Open a browser and go to http://localhost:8000 to see the website.

## Adding Facebook Integration
The Javascript required to log in to Facebook is included in this application.  However, you will need to apply for your own application on Facebook at their [Developer Site](http://developers.facebook.com/).  Once this is done, it is recommended that you add this to the local_settings.py file.  These settings can be added to settings.py, but be aware that a) this file is in public version control, and you don't want others knowing your secret keys and b) subsequent updates may reset the settings.py file.

<pre>
<code>
FACEBOOK_APP_ID = '&lt;APP_ID&gt;'
FACEBOOK_API_KEY = '&lt;API_KEY&gt;'
FACEBOOK_SECRET_KEY = '&lt;SECRET_KEY&gt;'
</code>
</pre>

These can be found in your application's page within the Facebook Developer page.

## Running tests
While Django/Pinax has support for running tests, some of the out of the box tests fail (as of Pinax 0.7.1).  You can run the tests using `python manage.py test`.  I created my own script to only run my own tests in the system.  You can run those tests by typing `python runtests.py`.  These are the same tests that are run by our continuous integration server.

## Other resources

Here are some online Python books that may be helpful when learning the language.

* Dive Into Python: Used to be online, but it has been taken down.
* [Learn Python the Hard Way](http://learnpythonthehardway.org/index) (more geared toward people new to coding)

The following tutorials may be helpful when learning about Django and the various packages used by the system.

* [Django Tutorial](http://docs.djangoproject.com/en/dev/intro/tutorial01/)
* [South Tutorial](http://south.aeracode.org/docs/tutorial/part1.html)

## Further documentation
Consult the [Wiki] (https://github.com/csdl/makahiki/wiki).
