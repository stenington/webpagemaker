import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

def slurp(fromdir, stdout, project_filter):
    projects = [
      dirname for dirname in os.listdir(fromdir)
      if os.path.isdir(os.path.join(fromdir, dirname))
      and not dirname.startswith('.')
      ]
    
    if project_filter:
        projects = filter(lambda n: n in project_filter, projects)
    
        if len(projects) is 0:
            stdout.write('Could not find any projects that match the filters %s.\n'
                         % str(project_filter))
            exit(1)

        if len(projects) != len(project_filter):
            stdout.write('WARNING: did not match all filters, %s\n' % str(project_filter))
    
    mydir = os.path.dirname(__file__)
    appdir = os.path.normpath(os.path.join(mydir, '..', '..'))
    templatedir = os.path.join(appdir, 'templates', 'learning_projects')
    for project in projects:
        stdout.write('Processing template for project "%s".\n' % project)
        filename = '%s.html' % project
        dirname = os.path.join(fromdir, project)
        html = open(os.path.join(dirname, filename)).read()
        html = html.replace('static/', '{{ HTTP_STATIC_URL }}%s/' % project)
        f = open(os.path.join(templatedir, filename), 'w')
        f.write(html)
        f.close()

        stdout.write('Processing static files for project "%s".\n' % project)
        staticdir = os.path.join(appdir, 'static', project)
        if os.path.exists(staticdir):
            shutil.rmtree(staticdir)
        shutil.copytree(os.path.join(dirname, 'static'), staticdir)
    stdout.write("Done.\n")

class Command(BaseCommand):
    args = '[project_name, project_name, ...]'
    help = 'Copies files from the learning projects dropbox into ' \
           'the learning_projects django app'

    def handle(self, *args, **options):
        if not hasattr(settings, 'LEARNING_PROJECTS_PATH'):
            raise CommandError("Please set the LEARNING_PROJECTS_PATH " \
                               "setting to point to the learning " \
                               "projects dropbox.")
        slurp(fromdir=settings.LEARNING_PROJECTS_PATH, stdout=self.stdout, project_filter=args)
        self.stdout.write("You should probaby run 'git status' now.\n")
