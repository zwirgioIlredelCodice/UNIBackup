REMOTE_NAME = 'unibackup'
REMOTE_DIR = REMOTE_NAME + ':unibackup/current/'
REMOTE_TYPE = 'onedrive'

MAINFILE_NAME = '.unibackup'
MAINFILE_DEFAULT = '''
{
    "last_push": "never"
    "last_pull": "never"
    "last_sync": "never"
}
'''
MAINFILE_PATH = MAINFILE_NAME

EXCLUDEFILE_NAME = '.unibackup_ignore'
EXCLUDEFILE_DEFAULT = ""
EXCLUDEFILE_PATH = EXCLUDEFILE_NAME
