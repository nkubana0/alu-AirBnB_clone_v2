#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create the folder if it doesn't exist
        local("mkdir -p versions")

        # Get the current date and time
        now = datetime.now()

        # Create the name of the archive file
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        # Create the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the archive
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None
