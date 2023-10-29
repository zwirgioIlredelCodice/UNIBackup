import os.path
import module.config.backup as cb
import module.rclone as rclone


def is_backup_dir(path):
    return os.path.exists(os.path.join(path, cb.MAINFILE_PATH))


def is_configured():
    return rclone.remote_exists(cb.REMOTE_NAME)


def config():
    if not is_configured():
        rclone.config()


def init(path):
    if not is_backup_dir():
        # create two empty files
        open(os.path.join(path, cb.MAINFILE_PATH), 'x')
        open(os.path.join(path, cb.EXCLUDEFILE_PATH), 'x')


def get_source_dest(path):
    source = os.path.abspath(path)
    dest = cb.REMOTE_DIR + os.path.basename(path)  # /folder not /folder/
    return source, dest


def copy(path):
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.copy(source, dest)


def upload(path):
    """
    similar to git push
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.sync(source, dest)


def download(path):
    """
    similar to git pull
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.sync(dest, source)


def sync(path):
    """
    similar to git pull
    """
    if is_backup_dir():
        source, dest = get_source_dest(path)
        rclone.bisync(source, dest)
