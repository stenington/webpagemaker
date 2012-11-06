import os
import re
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

try:
    LEARNING_PROJECTS_PATH = settings.LEARNING_PROJECTS_PATH
except AttributeError:
    LEARNING_PROJECTS_PATH = None

def rebase_static_urls(html, url):
    return re.sub(r'(?<!/)static/', url, html)

def slurp(fromdir, stdout, project_names):
    projects = [
      dirname for dirname in os.listdir(fromdir)
      if os.path.isdir(os.path.join(fromdir, dirname))
      and not dirname.startswith('.')
      ]
    
    if project_names:
        projects = filter(lambda n: n in project_names, projects)
    
        if len(projects) is 0:
            msg = 'Could not find any projects that match the filters %s.\n'
            raise CommandError(msg % str(project_names))

        if len(projects) != len(project_names):
            stdout.write('WARNING: did not match all filters, %s\n'
                         % str(project_names))
    
    mydir = os.path.dirname(__file__)
    appdir = os.path.normpath(os.path.join(mydir, '..', '..'))
    templatedir = os.path.join(appdir, 'templates', 'learning_projects')
    for project in projects:
        stdout.write('Processing template for project "%s".\n' % project)
        filename = '%s.html' % project
        dirname = os.path.join(fromdir, project)
        html = open(os.path.join(dirname, filename)).read()
        html = rebase_static_urls(html, '{{ HTTP_STATIC_URL }}%s/' % project)
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
    option_list = BaseCommand.option_list + (
        make_option('--path',
            default=LEARNING_PROJECTS_PATH,
            help='Override the learning projects path'),
        )
    help = 'Copies files from the learning projects dropbox into ' \
           'the learning_projects django app'
    
    def handle(self, *args, **options):
        if not options['path']:
            raise CommandError("Please set the LEARNING_PROJECTS_PATH " \
                               "setting to point to the learning " \
                               "projects dropbox or pass it in with --path")
        slurp(fromdir=options['path'], stdout=self.stdout, project_names=args)
        self.stdout.write("You should probaby run 'git status' now.\n")
