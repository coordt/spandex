import os

from settings import VIRTUALENV_ROOT, CURRENT_SITE, REQUIREMENTS_PATH

VENV = _join_path(VIRTUALENV_ROOT, CURRENT_SITE)

def _join_path(*args):
    """
    Join a set of paths
    """
    return os.path.abspath(os.path.normpath(os.path.join(*args)))

def install_pkg(package, version=None):
    """
    Install a package. Ideally should be in the format pkgname==vnum
    """
    from settings import EXTRA_INDEXES
    import re
    
    if not hasattr(env, 'updated_reqs'):
        set_env(updated_reqs=False)
    
    pip = "%sbin/python %sbin/pip -q install" % (VENV, VENV)
    virtenv = "-E %s" % venv
    extra_idx = " ".join("--extra-index-url=%s" % x for x in EXTRA_INDEXES)
    if version is None:
        pkg = package
    else:
        pkg = "%s==%s" % (package, version)
    cmd = [pip, virtenv, extra_idx, pkg]
    extra_msg = run(" ".join(cmd))
    if not env.updated_reqs:
        pkg_re = re.compile(r'%s\s*==\s*.+' % package)
        current_reqs = open('requirements.txt').read()
        if pkg_re.search(current_reqs):
            print "Updating %s entry to version %s in the requirements file..." % (package, version)
            new_reqs = pkg_re.sub(pkg, current_reqs)
        else:
            print "Adding %s entry in the requirements file..."
            new_reqs = current_reqs.strip('\n') + '\n' + pkg
        try:
            reqs_file = open('requirements.txt', 'w')
            reqs_file.write(new_reqs)
            set_env(updated_reqs = True)
        except IOError:
            print "Couldn't write to the requirements file."
        
        reqs_file.close()
    
    send_convore_update(msg="Install Package", extra=extra_msg)

@runs_once
def install_pkg_local(package, version):
    pip = "pip -q install"
    extra_idx = "--extra-index-url=http://opensource.washingtontimes.com/simple/"
    pkg = package if version is None else f"{package}=={version}"
    cmd = [pip, extra_idx, pkg]
    local(" ".join(cmd))

def pkg_version(package):
    """
    Print out the version installed for a particular package
    """
    run(f"{venv}bin/pip freeze | grep {package}")

def update_reqs():
    """
    Have pip install the requirements file. This will update any dependencies
    that have changed in the requirements file.
    """
    
    req_path = join_path(VIRTUALENC_ROOT, CURRENT_SITE, REQUIREMENTS_PATH)
    run(f'{venv}/bin/pip install -E {venv} -r {req_path}')

def reload():
    """
    Reload the apache process by touching the wsgi file
    """
    global site_path,wsgi_path
    with cd(site_path):
        run(f'touch {wsgi_path}')

def update():
    """
    Cause the site to pull in the latest changes to its code and touch the
    wsgi file so it reloads
    """
    global site_path
    with cd(site_path):
        extra_msg = run('git pull --all')
    reload()
    send_convore_update(msg="Push Live", extra=extra_msg)
