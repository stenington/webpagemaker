import os

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

from webpagemaker.api import sanitize, domdiff

def scan(fromdir, stdout):
    projects = [
      dirname for dirname in os.listdir(fromdir)
      if os.path.isdir(os.path.join(fromdir, dirname))
      and not dirname.startswith('.')
      ]
    for project in projects:
        filename = '%s.html' % project
        dirname = os.path.join(fromdir, project)
        html = open(os.path.join(dirname, filename)).read()
        sanitized = sanitize.sanitize(html)
        stripped = domdiff.diff(html, sanitized)
        if stripped:
            s = ", ".join(stripped)
            stdout.write('\nStripped in project "%s": %s\n' % (project, s))
        else:
            stdout.write('In project "%s", nothing is stripped.\n' % project)
        
    stdout.write("Done.\n")

class Command(NoArgsCommand):
    help = 'Scans files from the learning projects dropbox and ' \
           'detects possible sanitization problems.'

    def handle_noargs(self, *args, **options):
        if not hasattr(settings, 'LEARNING_PROJECTS_PATH'):
            raise CommandError("Please set the LEARNING_PROJECTS_PATH " \
                               "setting to point to the learning " \
                               "projects dropbox.")
        scan(fromdir=settings.LEARNING_PROJECTS_PATH, stdout=self.stdout)
