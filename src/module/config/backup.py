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
LOCALFILE_DEFAULT = json.dumps({first_sync: True}, indent=4)

LOCALFILE_PATH = LOCALFILE_NAME

EXCLUDEFILE_NAME = '.unibackup_ignore'
EXCLUDEFILE_DEFAULT = '/' + LOCALFILE_NAME
EXCLUDEFILE_PATH = EXCLUDEFILE_NAME


class OptionFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = module.utility.json_file_load(filename)

    def __del__(self):
        module.utility.json_file_save(self.filename, self.data)

    def get(self, name: str):
        return self.data[name]

    def set(self, name: str, value):
        self.data[name] = value

    def update(self, name: str, value):
        self.set(name, value)


class Localfile(OptionFile):
    def __init__(self):
        super().__init__(LOCALFILE_PATH)

    def __del__(self):
        super().__del__()

    def is_first_sync(self) -> bool:
        super().get(first_sync)

    def remember_sync(self):
        super().set(first_sync, False)
