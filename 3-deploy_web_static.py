#!/usr/bin/python3
"""
With Fabric, creates a tgz archive
from web_static content folder
"""

import argparse
from fabric.api import local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['54.165.70.250', '54.237.15.33']


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Deploy web static using Fabric")
    parser.add_argument("-i", "--identity", required=True, help="Path to SSH private key file")
    parser.add_argument("-u", "--username", required=True, help="SSH username")
    return parser.parse_args()

def do_pack():
    """Creates a tgz archive using fabric"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        filename = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {filename} web_static")
        return filename
    except Exception as ex:
        return None

def do_deploy(archive_path, username):
    """Deploy web static with fabric"""
    if exists(archive_path) is False:
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_excep = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run(f"sudo mkdir -p {path}{no_excep}")
        run(f"sudo tar -xzf /tmp/{filename} -C {path}{no_excep}")
        run(f"sudo rm /tmp/{filename}")
        run(f"sudo mv {path}{no_excep}/web_static/* {path}{no_excep}/")
        run(f"sudo rm -rf {path}{no_excep}/web_static")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {path}{no_excep}/ /data/web_static/current")
        return True
    except BaseException:
        return False

def deploy():
    """Do pack and deploy"""
    args = parse_arguments()
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path, args.username)

