import subprocess
import module.config.rclone as c


def shell(commands, get=False):
    if get:
        return subprocess.run(commands,
                              stdout=subprocess.PIPE,
                              text=True)
    else:
        return subprocess.run(commands)


def command(kind, args=[], options=[]):
    # if is not an array, make it
    if not (kind is list):
        kind = [kind]

    return [c.RCLONE] + kind + args + options


def version():
    version_number_i = 1

    version = shell(command(c.VERSION), get=True).stdout
    version = version.split()
    version = version[version_number_i]
    version = version.replace('v', '')
    version = version.replace('.', '', 10)
    return int(version)


def config():
    shell(command(c.CONFIG))


def copy(source, dest):
    """
    Copy the source to the destination. Does not transfer files that are
    identical on source and destination, testing by size and modification
    time or MD5SUM. Doesn't delete files from the destination. If you want
    to also delete files from destination, to make it match source, use
    the sync command instead.
    """
    shell(command(c.COPY, args=[source, dest]))


def sync(source, dest):
    """
    Sync the source to the destination, changing the destination only. Doesn't
    transfer files that are identical on source and destination, testing by
    size and modification time or MD5SUM. Destination is updated to match
    source, including deleting files if necessary (except duplicate objects,
    see below). If you don't want to delete files from destination, use the
    copy command instead.
    """
    shell(command(c.SYNC, args=[source, dest]))


def bisync(source, dest):
    """
    Perform bidirectional synchronization between two paths.

    Bisync provides a bidirectional cloud sync solution in rclone.
    It retains the Path1 and Path2 filesystem listings from the prior run.

    On each successive run it will:
    * list files on Path1 and Path2, and check for changes on each side.
        Changes include New, Newer, Older, and Deleted files.
    * Propagate changes on Path1 to Path2, and vice-versa.
    """
    shell(command(c.BISYNC, args=[source, dest]))
