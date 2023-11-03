RCLONE = 'rclone'
VERSION = '--version'

REMOTE_ADD = ['config', 'create']
REMOTE_DELETE = ['config', 'delete']
REMOTE_RECONNECT = ['config', 'reconnect']

MKDIR = 'mkdir'

COPY = ['copy', '--progress', '--verbose']
SYNC = ['sync', '--progress', '--verbose']
BISYNC = ['bisync', '--resync', '--progress', '--verbose'] # TODO: For successive sync runs, leave off the --resync flag
