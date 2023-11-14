
RCLONE = 'rclone'
VERSION = '--version'

REMOTE_ADD = ['config', 'create']
REMOTE_DELETE = ['config', 'delete']
REMOTE_RECONNECT = ['config', 'reconnect']

MKDIR = 'mkdir'

# exclude = ['--filter-from', exludefile.EXCLUDEFILE_PATH]
# exclude_bisync = ['--filters-file', exludefile.EXCLUDEFILE_PATH]

COPY = 'copy'
"""
def COPY(src: str, dst: str, excludef=True) -> list[str]:
    out = ['copy', src, dst, '--progress', '--verbose']
    if excludef:
        out = out + exclude
    return out
"""

SYNC = 'sync'
"""
def SYNC(src: str, dst: str) -> list[str]:
    return ['sync', src, dst, '--progress', '--verbose'] + exclude
"""

BISYNC = 'bisync'
""""
def BISYNC(src: str, dst: str) -> list[str]:
    return ['bisync', src, dst, '--progress', '--verbose'] + exclude_bisync
"""

CHECK = 'check'
""""
def CHECK(src: str, dst: str) -> list[str]:
    return ['check', src, dst] + exclude
"""


CLEANUP = 'cleanup'
""""
def CLEANUP(remotepath: str) -> list[str]:
    return ['cleanup', remotepath, '--verbose']
"""

LSJSON = 'lsjson'
""""
def LSJSON(path: str) -> list[str]:
    return ['lsjson', path]
"""

# OPTIONS
verbose = '--verbose'
progress = '--progress'
filter_from = '--filter-from'
filters_file = '--filters-file'
resync = '--resync'
