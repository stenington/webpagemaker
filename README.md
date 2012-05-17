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
  * python-dev
  * python-pip

To install `virtualenv`, run `sudo pip install virtualenv`.

(Python itself comes installed with Ubuntu, you will not need to
install this separately. In fact, doing so may cause problems)

#### Setting up webpagemaker

Once all prerequisites are installed, run the following commands:

    git clone --recursive git://github.com/mozilla/webpagemaker.git
    cd webpagemaker
    virtualenv .virtualenv
    source .virtualenv/bin/activate

Proceed with the installation by running the following commands in the 
webpagemaker directory:

    pip install -r requirements/compiled.txt
    cp webpagemaker/settings/local.py-dist webpagemaker/settings/local.py

At this point you'll want to edit the `local.py` file, which
contains all the settings used when talking to the MySQL instance,
including login credentials.

If you want to use the default database mentioned there, `playdoh_app`,
you can create it using this command:

    mysql -u root -e 'create database playdoh_app;'

OR by using this command, if your MySQL is password protected:

    mysql -u root -pYourPassWordHere -e 'create database playdoh_app;'

Then, synchronize the tables and initial data:

    python manage.py syncdb

Note that you might get prompted to create a superuser. If you do, go
ahead and make one, since you can use the admin interface to manage
your pages.

Then, bust up the initial migrations:

    python manage.py migrate

Finally, start the development server:

    python manage.py runserver

You can view the development server at http://localhost:8000/.

Whenever you create a new terminal session, you'll need to re-run
`source .virtualenv/bin/activate` to activate your virtualenv.

  [mysql]: http://dev.mysql.com/downloads/
  [virtualenv]: http://pypi.python.org/pypi/virtualenv

## Troubleshooting

### Mac OS X

#### Developer Tools

If you get errors claiming that `install_name_tool` or `gcc` can't be
found, make sure you have either XCode or the
[Apple command-line tools][osxcli].

  [osxcli]: https://developer.apple.com/downloads/index.action?=command%20line%20tools

#### MySQL

If you get the following error:

```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: dlopen(/Users/.../site-packages/_mysql.so, 2): Library not loaded: libmysqlclient.18.dylib
  Referenced from: /Users/.../site-packages/_mysql.so
  Reason: image not found
```

You will need to add the path to your `_mysql.so` to `DYLD_LIBRARY_PATH` in
your `~/.profile` like this:

```
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/local/mysql/lib
```

Note that you may also need to put MySQL's `bin` directory on your `PATH`
like so:

```
export PATH=$PATH:/usr/local/mysql/bin
```

## Other READMEs

Some of the Django apps in this project have their own README:

  * [webpagemaker/learning_projects/README.md](webpagemaker/tree/development/webpagemaker/learning_projects#readme)
  * [webpagemaker/api/README.md](webpagemaker/tree/development/webpagemaker/api#readme)

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
