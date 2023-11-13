import os.path
import module.config.backup as cb
import module.rclone as rclone


class Backup:
    def __init__(self, path):
        self.path = path
        self.source, self.dest = self.get_source_dest()

    def get_source_dest(self) -> (str, str):
        """map a local path with a remote path"""
        source = os.path.abspath(self.path)
        dest = cb.REMOTE_DIR + os.path.basename(self.path)  # /folder not /folder/
        return source, dest

    def is_backup_dir(self) -> bool:
        """ check if a directory is configured for unibackup

        Returns:
            bool: True if is a directory configured for unibackup, False otherwise
        """
        return os.path.exists(os.path.join(self.path, cb.MAINFILE_PATH))

    def is_configured(self) -> bool:
        """check if is properly configured

        Returns:
            bool: True if is properly configured, False otherwise
        """
        return rclone.remote_exists(cb.REMOTE_NAME)

    def config(self):
        """configure csunibackup"""
        if not self.is_configured():
            rclone.remote_add(cb.REMOTE_NAME, cb.REMOTE_TYPE)
        else:
            # if is configured, readd the remote, useful when is expired
            rclone.remote_delete(cb.REMOTE_NAME)
            rclone.remote_add(cb.REMOTE_NAME, cb.REMOTE_TYPE)

        # make csunibackup/ path in the remote
        rclone.mkdir(cb.REMOTE_DIR)

    def init(self):
        """ initialize unibakcup in the given path"""
        if not self.is_backup_dir():
            # create unibackup files
            f1 = open(os.path.join(self.path, cb.MAINFILE_PATH), 'w')
            f1.write(cb.MAINFILE_DEFAULT)
            f1.close()

            f2 = open(os.path.join(self.path, cb.EXCLUDEFILE_PATH), 'w')
            f2.write(cb.EXCLUDEFILE_DEFAULT)
            f2.close()

            f3 = open(os.path.join(self.path, cb.LOCALFILE_PATH), 'w')
            f3.write(cb.LOCALFILE_DEFAULT)
            f3.close()

    def listbakups(self):
        if self.is_configured():
            data = rclone.lsjson(cb.REMOTE_DIR, filters=['Name', 'IsDir'])

            print("list of folders saved in remote:")
            for d in data:
                if d['IsDir']:
                    print(d['Name'])

    def clone(self, remote_dir: str):
        """clone a remote unibackup directory in a respective local folder
        """
        remote = os.path.join(cb.REMOTE_DIR, remote_dir)
        local = os.path.join(self.path, remote_dir)
        rclone.mkdir(local)

        rclone.copy(remote, local, excludef=False)

    def safepush(self):
        """perform a rclone.copy of a local path to the remote"""
        if self.is_backup_dir():
            rclone.copy(self.source, self.dest)
        else:
            raise Exception("unibackup is not initialized in this directory")

    def safepull(self):
        """perform a rclone.copy from the remote to local"""
        if self.is_backup_dir():
            rclone.copy(self.dest, self.source)
        else:
            raise Exception("unibackup is not initialized in this directory")

    def push(self):
        """perform a rclone.sync of a local path to the remote
        similar to git push
        """
        if self.is_backup_dir():
            rclone.sync(self.source, self.dest)
        else:
            raise Exception("unibackup is not initialized in this directory")

    def pull(self):
        """perform a rclone.sync of remote into a local path
        similar to git pull
        """
        if self.is_backup_dir():
            rclone.sync(self.dest, self.source)
        else:
            raise Exception("unibackup is not initialized in this directory")

    def sync(self):
        """perform a rclone.bisync of a local path to the remote
        similar to git pull & push
        """
        settings = cb.Localfile()

        if self.is_backup_dir():
            if settings.is_first_sync():
                rclone.mkdir(self.dest)
                rclone.bisync(self.source, self.dest, options=['--resync'])
                settings.remember_sync()
            else:
                try:
                    rclone.bisync(self.source, self.dest)
                except:
                    # when updating .unibakcup_ignore
                    print('\nretry with --resync')
                    rclone.bisync(self.source, self.dest, options=['--resync'])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def status(self):
        if self.is_backup_dir():
            rclone.check(self.source, self.dest)
        else:
            raise Exception("unibackup is not initialized in this directory")
