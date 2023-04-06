#!/usr/bin/python3
"""
Fabric script generates .tgz archive of all in web_static folder.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create a compressed archive of the web_static directory.

    Returns:
        If the archive is created successfully, the path to the archive file
        is returned. Otherwise, None is returned.
    """
    # Get the current date and time
    cur_time = datetime.now()

    # Format the date and time as a string that can be used in the filename
    timestamp = cur_time.strftime("%Y%m%d%H%M%S")

    # Define the filename of the archive file
    archive_filename = "versions/web_static_{}.tgz".format(timestamp)

    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Create the archive file using the tar command
        local("tar -czvf {} web_static/".format(archive_filename))

        # If the archive is created successfully, return the path to the file
        return archive_filename

    except BaseException:
        # If an error occurs during the process of creating the archive file,
        # return None to indicate that something went wrong.
        return None
