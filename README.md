This is the Mozilla Webpage Maker project.

Currently our [prototype stub API][] is hosted at [webpagemakerapi.vcap.mozillalabs.com][].

We will be using [slowparse][] to assist users in editing their HTML.

This repository was originally forked from [playdoh][]. See its full [documentation][docs] for more help.

  [slowparse]: https://github.com/toolness/slowparse#readme
  [prototype stub API]: https://github.com/mozilla/webpagemaker/tree/development/prototype/api#readme
  [webpagemakerapi.vcap.mozillalabs.com]: http://webpagemakerapi.vcap.mozillalabs.com/
  [docs]: http://playdoh.rtfd.org/
  [playdoh]: https://github.com/mozilla/playdoh

## Getting Started

Before embarking on setting up this app, you will want to install
[mysql][]. In particular, make sure that `mysql_config` is an
executable on your `PATH`.

You'll also want to get [virtualenv][].

### Installing the prerequisites on Ubuntu

Use `sudo apt-get install <packagename>` to install the following
packages (it is always a good idea to run `sudo apt-get update` to
make sure you will be receiving the most up to date repository list
before installing):

  * mysql-server
  * libmysqlclient-dev
  * python
  * python-dev
  * python-pip

To install `virtualenv`, run `sudo pip install virtualenv`.

#### Setting up webpagemaker

Once all prerequisites are install, run the following commands:

    git clone --recursive git://github.com/mozilla/webpagemaker.git
    cd webpagemaker
    virtualenv .virtualenv
    source .virtualenv/bin/activate
    pip install -r requirements/compiled.txt
    cp webpagemaker/settings/local.py-dist webpagemaker/settings/local.py

At this point you'll want to edit the `local.py` file, which
contains all the settings used when talking to the MySQL instance,
including login credentials.

If you want to use the default database mentioned there, `playdoh_app`,
you can create it using this command:

    mysql -u root -e 'create database playdoh_app;'

Then, synchronize the tables and initial data:

    python manage.py syncdb

Finally, start the development server:

    python manage.py runserver

You can view the development server at http://localhost:8000/.

Whenever you create a new terminal session, you'll need to re-run
`source .virtualenv/bin/activate` to activate your virtualenv.

  [mysql]: http://dev.mysql.com/downloads/
  [virtualenv]: http://pypi.python.org/pypi/virtualenv

## Other Resources

  * [Official Project Status Page](https://wiki.mozilla.org/Webpagemakerapi)
  * [Weekly Call Info](https://wiki.mozilla.org/WebPageMaker)
  * [Google Group](http://groups.google.com/group/mozwebpagemaker/topics?hl=en](http://groups.google.com/group/mozwebpagemaker/topics?hl=en)

## Etherpads

  * [webpagemaker-meeting](https://etherpad.mozilla.org/webpagemaker-meeting)
  * [webmaker-for-summer-campaign](https://etherpad.mozilla.org/webmaker-for-summer-campaign)
  * [webpagemaker-pitch](https://etherpad.mozilla.org/webpagemaker-pitch)
  * [design-principles](https://mozlearning.etherpad.mozilla.org/design-principles)
  * [webmaker-rfc](https://etherpad.mozilla.org/webmaker-rfc)
  * [assessment-builder](https://etherpad.mozilla.org/assessment-builder)

## License

This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

  [BSD]: http://creativecommons.org/licenses/BSD/
