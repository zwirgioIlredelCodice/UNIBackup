import module.config.backup as exludefile

RCLONE = 'rclone'
VERSION = '--version'

REMOTE_ADD = ['config', 'create']
REMOTE_DELETE = ['config', 'delete']
REMOTE_RECONNECT = ['config', 'reconnect']

MKDIR = 'mkdir'

exclude = '--filter-from '+exludefile.EXCLUDEFILE_PATH
exclude_bisync = '--filters-file '+exludefile.EXCLUDEFILE_PATH


def COPY(src: str, dst: str) -> list[str]:
    return ['copy', src, dst, '--progress', '--verbose', exclude]


def SYNC(src: str, dst: str) -> list[str]:
    return ['sync', src, dst, '--progress', '--verbose', exclude]


def BISYNC(src: str, dst: str) -> list[str]:
    return ['bisync', src, dst, '--verbose', exclude_bisync]
