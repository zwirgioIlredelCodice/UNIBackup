import os.path
import module.rclone as rclone


class Settings:
    import module.utility
    import json

    REMOTE_NAME = 'unibackup'
    REMOTE_DIR = REMOTE_NAME + ':unibackup/current/'
    REMOTE_TYPE = 'onedrive'

    MAINFILE_NAME = '.unibackup'
    MAINFILE_DEFAULT = ''
    MAINFILE_PATH = MAINFILE_NAME

    LOCALFILE_NAME = '.unibackup_local'

    first_sync = 'first_sync'
    LOCALFILE_DEFAULT = json.dumps(
        {
            first_sync: True
        },
        indent=4)

    LOCALFILE_PATH = LOCALFILE_NAME

    EXCLUDEFILE_NAME = '.unibackup_ignore'
    EXCLUDEFILE_DEFAULT = '''
    # EXCLUDE

    # do not touch the next line
    - /.unibackup_local

    # put your exclude here
    # - .git/ (example)
    '''
    EXCLUDEFILE_PATH = EXCLUDEFILE_NAME

    class Localfile(module.utility.OptionFile):
        def __init__(self):
            super().__init__(self.LOCALFILE_PATH)

        def __del__(self):
            super().__del__()

        def is_first_sync(self) -> bool:
            return super().get(self.first_sync)

        def remember_sync(self):
            super().set(self.first_sync, False)


class Backup:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.local = self.path
        self.remote = self.local_to_remote(self.path)

        self.exludefile_local = self.local_to_local(Settings.EXCLUDEFILE_PATH)
        self.exludefile_remote = os.path.join(self.remote, Settings.EXCLUDEFILE_PATH)

    def local_to_local(self, path: str) -> str:
        return os.path.join(self.path, path)

    def local_to_remote(self, path: str) -> str:
        return os.path.join(Settings.REMOTE_DIR, os.path.basename(path))

    def remote_to_remote(self, path: str) -> str:
        return os.path.join(Settings.REMOTE_DIR, path)

    def create_mainfile(self):
        f = open(self.local_to_local(Settings.MAINFILE_PATH), 'w')
        f.write(Settings.MAINFILE_DEFAULT)
        f.close()

    def create_excludefile(self):
        f = open(self.local_to_local(Settings.EXCLUDEFILE_PATH), 'w')
        f.write(Settings.EXCLUDEFILE_DEFAULT)
        f.close()

    def create_localfile(self):
        f = open(self.local_to_local(Settings.LOCALFILE_PATH), 'w')
        f.write(Settings.LOCALFILE_DEFAULT)
        f.close()

    def is_backup_dir(self) -> bool:
        """ check if a directory is configured for unibackup

        Returns:
            bool: True if is a directory configured for unibackup, False otherwise
        """
        return os.path.exists(self.local_to_local(Settings.MAINFILE_PATH))

    def is_configured(self) -> bool:
        """check if is properly configured

        Returns:
            bool: True if is properly configured, False otherwise
        """
        return rclone.remote_exists(Settings.REMOTE_NAME)

    def config(self):
        """configure csunibackup"""
        if not self.is_configured():
            rclone.remote_add(Settings.REMOTE_NAME, Settings.REMOTE_TYPE)
        else:
            # if is configured, readd the remote, useful when is expired
            rclone.remote_delete(Settings.REMOTE_NAME)
            rclone.remote_add(Settings.REMOTE_NAME, Settings.REMOTE_TYPE)

        # make csunibackup/ path in the remote
        rclone.mkdir(Settings.REMOTE_DIR)

    def init(self):
        """ initialize unibakcup in the given path"""
        if not self.is_backup_dir():
            # create unibackup files
            self.create_mainfile()
            self.create_localfile()
            self.create_excludefile()

    def listbackups(self):
        if self.is_configured():
            data = rclone.lsjson(Settings.REMOTE_DIR, filters=['Name', 'IsDir'])

            print("list of folders saved in remote:")
            for d in data:
                if d['IsDir']:
                    print(d['Name'])

    def clone(self, remote_dir: str):
        """clone a remote unibackup directory in a respective local folder
        """
        remote = self.remote_to_remote(remote_dir)
        local = self.local_to_local(remote_dir)
        rclone.mkdir(local)
        exludefile_remote = os.path.join(remote, Settings.EXCLUDEFILE_PATH)

        rclone.copy(remote, local, options=[
            rclone.filter_from, exludefile_remote,
            rclone.progress,
            rclone.verbose
            ])

        self.create_localfile()

    def safepush(self):
        """perform a rclone.copy of a local path to the remote"""
        if self.is_backup_dir():
            rclone.copy(self.local, self.remote, options=[
                rclone.filter_from, self.exludefile_local,
                rclone.progress,
                rclone.verbose
                ])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def safepull(self):
        """perform a rclone.copy from the remote to local"""
        if self.is_backup_dir():
            rclone.copy(self.remote, self.local, options=[
                rclone.filter_from, self.exludefile_remote,
                rclone.progress,
                rclone.verbose
                ])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def push(self):
        """perform a rclone.sync of a local path to the remote
        similar to git push
        """
        if self.is_backup_dir():
            rclone.sync(self.local, self.remote, options=[
                rclone.filter_from, self.exludefile_local,
                rclone.progress,
                rclone.verbose
                ])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def pull(self):
        """perform a rclone.sync of remote into a local path
        similar to git pull
        """
        if self.is_backup_dir():
            rclone.sync(self.remote, self.local, options=[
                rclone.filter_from, self.exludefile_remote,
                rclone.progress,
                rclone.verbose
                ])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def sync(self):
        """perform a rclone.bisync of a local path to the remote
        similar to git pull & push
        """
        settings = Settings.Localfile()

        if self.is_backup_dir():
            if settings.is_first_sync():
                rclone.mkdir(self.remote)
                rclone.bisync(self.local, self.remote, options=[
                    rclone.resync,
                    rclone.filters_file, self.exludefile_local,
                    rclone.progress,
                    rclone.verbose
                    ])
                settings.remember_sync()
            else:
                try:
                    rclone.bisync(self.local, self.remote, options=[
                        rclone.filters_file, self.exludefile_local,
                        rclone.progress,
                        rclone.verbose
                        ])
                except:
                    # when updating .unibakcup_ignore
                    print('\nretry with --resync')
                    rclone.bisync(self.local, self.remote, options=[
                        rclone.resync,
                        rclone.filters_file, self.exludefile_local,
                        rclone.progress,
                        rclone.verbose
                        ])
        else:
            raise Exception("unibackup is not initialized in this directory")

    def status(self):
        if self.is_backup_dir():
            rclone.check(self.local, self.remote)
        else:
            raise Exception("unibackup is not initialized in this directory")
