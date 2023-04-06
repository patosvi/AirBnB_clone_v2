#!/usr/bin/python3
"""
Fabric bash script to deploy web static content
"""

from fabric.api import env, put, run
from os.path import exists
import os

env.hosts = ['100.26.142.215', '100.26.174.154']


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers
    """
    # Check if archive_path exists
    if not exists(archive_path):
        return False

    # Get the file name without extension
    archive_name = os.path.basename(archive_path)
    archive_name_no_ext = os.path.splitext(archive_name)[0]

    try:
        # Upload archive to the temporary folder on the web server
        put(archive_path, "/tmp/")

        # Create the directory where the code will be deployed
        run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(archive_name_no_ext))

        # Uncompress the archive into the deployment folder
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_name_no_ext))

        # Remove the archive from the server
        run("sudo rm /tmp/{}".format(archive_name))

        # Move the files to a new folder and delete the old symbolic link
        run("sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(archive_name_no_ext, archive_name_no_ext))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_name_no_ext))

        # Delete the old symbolic link and create a new one
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ \
                /data/web_static/current".format(archive_name_no_ext))

        return True

    except Exception as e:
        # If there is an error, return False
        return False
