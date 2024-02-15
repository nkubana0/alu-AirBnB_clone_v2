#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import run, env, lcd
from fabric.operations import local
import os

env.hosts = ['54.91.92.144', '52.87.244.116']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
    except ValueError:
        print("Error: Number must be an integer")
        return False

    if number < 0:
        print("Error: Number must be a positive integer")
        return False

    with lcd("versions"):
        archives_local = local("ls -t | grep '.tgz'", capture=True).split('\n')

        archives_to_keep_local = archives_local[:number]

        for archive in archives_local:
            if archive not in archives_to_keep_local:
                local("rm -f {}".format(archive))

    with cd("/data/web_static/releases"):
        archives_remote = run("ls -t | grep '.tgz'").split('\n')

        archives_to_keep_remote = archives_remote[:number]

        for archive in archives_remote:
            if archive not in archives_to_keep_remote:
                run("rm -f {}".format(archive))

    return True
