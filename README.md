This is the Mozilla ~~Webpage Maker~~ Thimble App project.
[![Build Status](https://secure.travis-ci.org/mozilla/webpagemaker.png?branch=development)](http://travis-ci.org/mozilla/webpagemaker)

We will be using [slowparse][] to assist users in editing their HTML.

This repository was originally forked from [playdoh][]. See its full [documentation][docs] for more help.

  [slowparse]: https://github.com/toolness/slowparse#readme
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

## Contributing

If you want to contribute to webpagemaker: great!

As webpagemaker is a github-hosted project, all you have to do is fork the repository to your own account, and start hacking on it. If you have any code you want to have merged into the main codebase, simply make sure it's in a branch of its own in your forked repository, and do a pull request onto our webpagemaker/development branch. We'll review the code, signal any potential problems there might be, and if there are no problems, merge it in!

If you're interested in hacking on any of the submodules, such as friendlycode or slowparse, you will want to fork those as well, as you should not be modifying the code for a submodule in a project that uses the submodule. Instead, fork them to your account, work on them, and then do pull requests for each code contribution you'd like to have merged into them. Whenever these submodule projects are updated, we updated the webpagemaker submodule pointers to point to the latest stable version.

Friendlycode is currently housed at https://github.com/toolness/friendlycode, and Slowparse can be found at https://github.com/toolness/slowparse.

## Other READMEs

Some of the Django apps in this project have their own README:

  * [webpagemaker/learning_projects/README.md](webpagemaker/tree/development/webpagemaker/learning_projects#readme)
  * [webpagemaker/api/README.md](webpagemaker/tree/development/webpagemaker/api#readme)

## Other Resources

  * [Official Project Status Page](https://wiki.mozilla.org/Webpagemakerapi)
  * [Weekly Call Info](https://wiki.mozilla.org/WebPageMaker)
  * [Google Group](http://groups.google.com/group/mozwebpagemaker/topics?hl=en](http://groups.google.com/group/mozwebpagemaker/topics?hl=en)
  * [Developer notes on working with development, staging, and production branches](https://github.com/mozilla/webpagemaker/wiki/Development,-Staging,-Production)

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
