import subprocess
import os

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def pull(request):
    """
    Endpoint for git post-commit hook.
    """
    
    git_root = os.path.join(os.path.dirname(__file__), '..', '..')
    subprocess.check_call(['git', 'pull'], cwd=git_root)
    subprocess.check_call(['git', 'submodule', 'update'], cwd=git_root)
    return HttpResponse('git pull succeeded')
