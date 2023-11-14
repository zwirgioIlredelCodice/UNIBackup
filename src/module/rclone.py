import subprocess

import module.config.rclone as c
import module.utility


def shell(commands: list[str], get=False, check=True):
    module.utility.prettyPrint.ok(' '.join(commands))
    """ execute shell commands

    Args:
        commands: command to execute represented as a list of str
        get: if True return the output of the runned command
    """
    if get:
        return subprocess.run(commands,
                              stdout=subprocess.PIPE,
                              text=True, check=check).stdout
    else:
        return subprocess.run(commands, check=check)


def command(kind: str | list[str], args=[], options=[]) -> list[str]:
    """ assemble a rclone command

    Args:
        kind: an str or a list of str representing a rclone subcommand
        args: optional arguments
        options: optional options

    Returns:
        list[str]: a command ready to be executed with shell()
    """
    # if is not an array, make it
    if not (type(kind) is list):
        kind = [kind]

    return [c.RCLONE] + kind + args + options


def version() -> str:
    """ get rclone version number

    Returns:
        str: rclone version
    """
    version_number_i = 1

    version = shell(command(c.VERSION), get=True)
    version = version.split()
    version = version[version_number_i]
    return version


def listremotes() -> list[str]:
    """ list all configured remotes

    Returns:
        list[str]: array of configured remotes names
    """
    out = shell(command("listremotes"), get=True)
    out = out.split()
    names = []
    # remove : at the end of each remote
    for s in out:
        names.append(s.rstrip(':'))

    return names


def remote_exists(remote_name: str) -> bool:
    """check if remote exists

    Args:
        remote_name: name of the remote to check

    Returns:
        bool: True if remote exists, false otherwise
    """
    return remote_name in listremotes()


def remote_add(remote_name: str, remote_type: str):
    """add a new remote

    Args:
        remote_name: name of the remote to add
        remote_type: type of the remote
    """
    shell(command(c.REMOTE_ADD, args=[remote_name, remote_type]))


def remote_delete(remote_name: str):
    """delete a remote

    Args:
        remote_name: name of the remote to delete
    """
    shell(command(c.REMOTE_DELETE, args=[remote_name]))


def remote_reconnect(remote_name: str):
    """reconnect a remote, usful when token expire

    Args:
        remote_name: name of the remote to reconnect
    """
    shell(command(c.REMOTE_RECONNECT, args=[remote_name]))


def mkdir(path: str):
    """Make the path if it doesn't already exist."""
    shell(command(c.MKDIR, args=[path]))


def copy(source: str, dest: str, options: list[str] = []):
    """
    Copy the source to the destination. Does not transfer files that are
    identical on source and destination, testing by size and modification
    time or MD5SUM. Doesn't delete files from the destination. If you want
    to also delete files from destination, to make it match source, use
    the sync command instead.

    Args:
        source: local path or remote path
        dest: local path or remote path
    """
    shell(command(c.COPY, args=[source, dest], options=options))


def sync(source: str, dest: str, options: list[str] = []):
    """
    Sync the source to the destination, changing the destination only. Doesn't
    transfer files that are identical on source and destination, testing by
    size and modification time or MD5SUM. Destination is updated to match
    source, including deleting files if necessary (except duplicate objects,
    see below). If you don't want to delete files from destination, use the
    copy command instead.

    Args:
        source: local path or remote path
        dest: local path or remote path
    """
    shell(command(c.SYNC, args=[source, dest], options=options))


def bisync(source: str, dest: str, options: list[str] = []):
    """
    Perform bidirectional synchronization between two paths.

    Bisync provides a bidirectional cloud sync solution in rclone.
    It retains the Path1 and Path2 filesystem listings from the prior run.

    On each successive run it will:
    * list files on Path1 and Path2, and check for changes on each side.
        Changes include New, Newer, Older, and Deleted files.
    * Propagate changes on Path1 to Path2, and vice-versa.

    Args:
        source: local path or remote path
        dest: local path or remote path
    """
    shell(command(c.BISYNC, args=[source, dest], options=options))


def check(source: str, dest: str, options: list[str] = []):
    """
    Checks the files in the source and destination match.
    It compares sizes and hashes (MD5 or SHA1) and logs a
    report of files that don't match. It doesn't alter the
    source or destination.

    Args:
        source: local path or remote path
        dest: local path or remote path
    """
    shell(command(c.CHECK, args=[source, dest], options=options))


def cleanup(remotepath: str, options: list[str] = []):
    """
    Clean up the remote if possible. Empty the trash or
    delete old file versions. Not supported by all remotes.

    Args:
        remotepath: path to a remote or a remote directory to clean
    """
    shell(command(c.CLEANUP, args=remotepath, options=options))


def lsjson(path: str, filters: list[str] = []) -> list[dict]:
    """
    List directories and objects in the path in JSON format.

    Args:
        path: remote or local path
        filters: array of filter, if [] all

    filters = {"Path","Name","Size","MimeType","ModTime","IsDir","ID"}
    """
    import json
    textdata = shell(command(c.LSJSON, args=[path]), get=True)
    data = json.loads(textdata)

    if len(filters) == 0:
        return data

    newlist = []
    for d in data:
        newdict = {}
        for f in filters:
            newdict[f] = d.get(f)
        newlist.append(newdict)

    return newlist



























