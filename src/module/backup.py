import os.path
import module.config.backup as cb
import module.rclone as rclone


def is_backup_dir(path: str) -> bool:
    """ check if a directory is configured for unibackup

    Args:
        path: path to a directory

    Returns:
        bool: True if is a directory configured for unibackup, False otherwise
    """
    return os.path.exists(os.path.join(path, cb.MAINFILE_PATH))


def is_configured() -> bool:
    """check if is properly configured

    Returns:
        bool: True if is properly configured, False otherwise
    """
    return rclone.remote_exists(cb.REMOTE_NAME)


def config():
    """configure csunibackup"""
    if not is_configured():
        rclone.remote_add(cb.REMOTE_NAME, cb.REMOTE_TYPE)
    else:
        # if is configured, readd the remote, useful when is expired
        rclone.remote_delete(cb.REMOTE_NAME)
        rclone.remote_add(cb.REMOTE_NAME, cb.REMOTE_TYPE)

    # make csunibackup/ path in the remote
    rclone.mkdir(cb.REMOTE_DIR)


def init(path: str):
    """ initialize unibakcup in the given path

    Args:
        path: directory to initialize
    """
    if not is_backup_dir():
        # create two empty files
        f1 = open(os.path.join(path, cb.MAINFILE_PATH), 'w')
        f1.write(cb.MAINFILE_DEFAULT)
        f1.close()
        f2 = open(os.path.join(path, cb.EXCLUDEFILE_PATH), 'w')
        f2.write(cb.EXCLUDEFILE_DEFAULT)
        f2.close()


def get_source_dest(path: str) -> (str, str):
    """map a local path with a remote path"""
    source = os.path.abspath(path)
    dest = cb.REMOTE_DIR + os.path.basename(path)  # /folder not /folder/
    return source, dest


def clone(remote_path: str, local_path: str):
    """clone a remote unibackup directory in a respective local folder

    Args:
        remote_path: unibackup directory in remote
                     es. analisi, not unibackup:unibackup/analisi
        local_path: local path where remote path content is cloned
                    es. /home/fabio
    """
    remote = os.path.join(cb.REMOTE_DIR, remote_path)
    local = os.path.join(local_path, remote_path)
    rclone.mkdir(local)

    rclone.copy(remote, local)


def copy(path: str):
    """perform a rclone.copy of a local path to the remote"""
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.copy(source, dest)


def push(path: str):
    """perform a rclone.sync of a local path to the remote
    similar to git push
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.sync(source, dest)


def pull(path):
    """perform a rclone.sync of remote into a local path
    similar to git pull
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.sync(dest, source)


def sync(path):
    """perform a rclone.bisync of a local path to the remote
    similar to git pull & push
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.bisync(source, dest)
