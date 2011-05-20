from __future__ import with_statement
import os

# from django.core import management
# # We have to re-name this to avoid clashes with fabric.api.settings.
# import settings as django_settings
# management.setup_environ(django_settings)

from fabric.api import *
# This will import every command, you may need to get more selective if
# you aren't using all of the stuff we do.
# For example:
# from fabtastic.fabric.commands.c_common import *
# from fabtastic.fabric.commands.c_git import git_pull
# from fabtastic.fabric.commands import *

import settings as fab_settings
attrs = [i for i in dir(fab_settings) if not i.startswith('__')]
for attr in attrs:
    setattr(env, attr, getattr(fab_settings, attr))

from deploy import *

def staging():
    """
    Sets env.hosts to the sole staging server. No roledefs means that all
    deployment tasks get ran on every member of env.hosts.
    """
    env.hosts = ['staging.example.com']

def prod():
    """
    Set env.roledefs according to our deployment setup. From this, an
    env.hosts list is generated, which determines which hosts can be
    messed with. The roledefs are only used to determine what each server is.
    """
    # Varnish proxies.
    env.roledefs['varnish_servers'] = ['varnish1.example.org', 'varnish2.example.org']
    # The Django app servers.
    env.roledefs['webapp_servers'] = ['app1.example.org', 'app2.example.org']
    # Static media servers
    env.roledefs['media_servers'] = ['media1.example.org']
    # Postgres servers.
    env.roledefs['db_servers'] = ['db1.example.org']

    # Combine all of the roles into the env.hosts list.
    env.hosts = [host[0] for host in env.roledefs.values()]
    