import module.config.backup as exludefile

RCLONE = 'rclone'
VERSION = '--version'

REMOTE_ADD = ['config', 'create']
REMOTE_DELETE = ['config', 'delete']
REMOTE_RECONNECT = ['config', 'reconnect']

MKDIR = 'mkdir'

exclude = '--filter-from '+exludefile.EXCLUDEFILE_PATH
exclude_bisync = '--filters-file '+exludefile.EXCLUDEFILE_PATH

COPY = ['copy', '--progress', '--verbose', exclude]
SYNC = ['sync', '--progress', '--verbose', exclude]

BISYNC = ['bisync', '--progress', '--verbose', exclude_bisync]
