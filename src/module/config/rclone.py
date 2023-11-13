import module.config.backup as exludefile

RCLONE = 'rclone'
VERSION = '--version'

REMOTE_ADD = ['config', 'create']
REMOTE_DELETE = ['config', 'delete']
REMOTE_RECONNECT = ['config', 'reconnect']

MKDIR = 'mkdir'

exclude = ['--filter-from', exludefile.EXCLUDEFILE_PATH]
exclude_bisync = ['--filters-file', exludefile.EXCLUDEFILE_PATH]


def COPY(src: str, dst: str, excludef=True) -> list[str]:
    out = ['copy', src, dst, '--progress', '--verbose']
    if excludef:
        out.append(exclude)
    return out


def SYNC(src: str, dst: str) -> list[str]:
    return ['sync', src, dst, '--progress', '--verbose'] + exclude


def BISYNC(src: str, dst: str) -> list[str]:
    return ['bisync', src, dst, '--progress', '--verbose'] + exclude_bisync


def CHECK(src: str, dst: str) -> list[str]:
    return ['check', src, dst] + exclude


def CLEANUP(remotepath: str) -> list[str]:
    return ['cleanup', remotepath, '--verbose']


def LSJSON(path: str) -> list[str]:
    return ['lsjson', path]
