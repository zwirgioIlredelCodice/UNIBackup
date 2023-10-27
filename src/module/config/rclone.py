import module.config.backup as bc

RCLONE = 'rclone'
VERSION = '--version'
CONFIG = ['config', 'create', bc.REMOTE_NAME, bc.REMOTE_TYPE]
COPY = ['copy', '--verbose', '--progress']
SYNC = ['sync', '--verbose', '--progress']
BISYNC = ['bisync', '--verbose', '--progress']
