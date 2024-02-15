#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['54.91.92.144', '54.91.92.144']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        local("mkdir -p versions")

        now = datetime.now()

        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[1]

        put(archive_path, '/tmp/{}'.format(archive_name))
        run('mkdir -p /data/web_static/releases/{}/'.format(
            archive_name[:-4]))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_name, archive_name[:-4]))
        run('rm /tmp/{}'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(
                archive_name[:-4], archive_name[:-4]))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_name[:-4]))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(archive_name[:-4]))

        return True
    except:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
