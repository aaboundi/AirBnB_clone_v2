#!/usr/bin/python3
"""Fabfile to distrubute an archive to a web server"""

from fabric.api import env, run, put
from datetime import datetime
from os.path import isfile


env.hosts = ['44.200.176.121', '44.200.77.205']


"""def do_pack():
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result
"""


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not isfile(archive_path):
        return False
    try:
        file_name = archive_path.split('/')[1]
        folder_name = file_name.split('.')[0]
        folder_path = "/data/web_static/releases/"

        put(archive_path, "/tmp/".format(file_name))
        run("sudo mkdir -p {}{}".format(folder_path, folder_name))
        run("sudo tar -xzf /tmp/{} -C {}{}".format(file_name, folder_path,
                                                   folder_name))
        run("sudo rm -rf /tmp/{}".format(file_name))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(folder_path,
                                                         folder_name))
        run("sudo rm -rf {}{}/web_static".format(folder_path, folder_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{} /data/web_static/current".format(folder_path,
                                                              folder_name))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return sucess
