This app contains templates and static files for [learning projects][].

Learning projects are originally created by our learning team, who are
familiar with HTML/CSS but unfamiliar with tools like git and Django.
As a result, the development and deployment of a learning project goes 
through different stages.

## Developing Missions

A project starts its life on Dropbox as a simple directory structure
like this:

    meme/
        meme.html
        static/
            seriouscat.jpg

Here we assume that `meme` is the unique name of the project; it is
represented by a folder with a single HTML file in it. This HTML
file represents the code that users when see when they undertake the
learning project.

All images, external CSS, fonts, and other resources referenced by
the learning project should be contained in the `static` subdirectory,
which itself can have more subdirectories.

## Productionalizing Missions

At some point, a developer should code review the missions and
import them into the playdoh project using the following command:

    python manage.py slurplearningprojects
    
This will take all the learning project folders contained in the
directory specified by `settings.LEARNING_PROJECTS_PATH` and copy
them into the `learning_projects` app. All static files will be
copied into the app's `static` folder, while each project's HTML file will be
converted into a template and placed in the app's `templates` folder.

All relative references to the `static` subdirectory in each
project's HTML file will be replaced with absolute URLs, ensuring that
the resulting HTML can be easily relocated without breaking links.

  [learning projects]: http://jessicaklein.blogspot.com/2012/04/curate-your-learning-through-webmaker.html