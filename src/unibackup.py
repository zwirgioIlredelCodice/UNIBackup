#!/usr/bin/env python3
import os

import module.rclone as rclone
import module.backup as backup

# TODO: better help
HELP = '''
Usage:
    unibackup [-h | --help] | <command> [<args>]

Commands:
    info    get some info about this program
    status  show the status of the running direcory
    config  configure unibackup
    init    initialize unibackup in the running direcory

    clone <ndir-name>   clone a unibackup direcory of the given name in the running direcory
    copy    backup files in the remote, does't delete files from the remote'
    push    sync the remote backup with the running direcory
    pull    sync local directory with the remote backup
    sync    perform bidirectional synchronization between local and remote backup
'''

if __name__ == "__main__":
    cwd = os.getcwd()

    import sys
    if len(sys.argv) <= 1:
        print(HELP)
        exit()

    args = sys.argv[1:]
    command = args[0]

    found_command = True

    if command in ['help', '--help', '-h']:
        print(HELP)
        exit()
    elif command == "config":
        backup.config()
    elif command == "init":
        if backup.is_backup_dir(cwd):
            print("alredy initialized")
        else:
            backup.init(cwd)
    elif command == "clone":
        backup.clone(args[1], cwd)
    else:
        found_command = False

    if not found_command and not backup.is_configured():
        # TODO: better error
        print('unibackup is not configured')
        print('run unibackup config')
        exit()
    if not found_command and not backup.is_backup_dir(cwd):
        # TODO: better error
        print('unibackup is not initialize in this directory')
        print('run unibackup init')
        exit()

    if command == "info":
        print("rclone version:", rclone.version())
    elif command == 'status':
        backup.status(cwd)
    elif command == "copy":
        backup.copy(cwd)
    elif command == "push":
        backup.push(cwd)
    elif command == "pull":
        backup.pull(cwd)
    elif command == "sync":
        backup.sync(cwd)
    else:
        if not found_command:
            print('command not found')
            print('run unibackup -h for help')
