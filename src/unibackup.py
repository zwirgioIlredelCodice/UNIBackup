#!/usr/bin/env python3
import os
import sys
import argparse
from functools import wraps

import module.rclone as rclone
from module.backup import Backup

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


def info():
    print("rclone version:", rclone.version())


if __name__ == "__main__":
    cwd = os.getcwd()
    backup = Backup(cwd)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    info_parser = subparsers.add_parser('info',
                                        help='get some info about this program')
    status_parser = subparsers.add_parser('status',
                                          help='show the status of the running direcory')
    config_parser = subparsers.add_parser('config', help='configure unibackup')
    init_parser = subparsers.add_parser('init',
                                        help='initialize unibackup in the running direcory')

    clone_parser = subparsers.add_parser('clone',
                                        help='clone a unibackup direcory in the running direcory')
    clone_parser.add_argument('-d', '--remote_dir', dest='remote_dir',
                              help='direcory name to clone')

    copy_parser = subparsers.add_parser('copy',
                                        help="backup files in the remote, does't delete files from the remote")
    push_parser = subparsers.add_parser('push',
                                        help="sync the remote backup with the running direcory")
    pull_parser = subparsers.add_parser('pull',
                                        help="sync local directory with the remote backup")
    sync_parser = subparsers.add_parser('sync',
                                        help="perform bidirectional synchronization between local and remote backup")


    # https://stackoverflow.com/questions/4575747/get-selected-subcommand-with-argparse
    kwargs = vars(parser.parse_args())
    subcommand = kwargs['subparser']

    if subcommand in ['status', 'copy', 'push', 'pull', 'sync']:
        if not backup.is_configured():
            print('unibackup is not configured')
            print('run unibackup config')
        if not backup.is_backup_dir():
            print('unibackup is not initialize in this directory')
            print('run unibackup init')
        else:
            # call backup.subcommand(**kwargs)
            globals()['backup' + kwargs.pop('subparser')](**kwargs)
    else:
        match subcommand:
            case 'info':
                globals()[kwargs.pop('subparser')](**kwargs)
            case 'config':
                globals()['backup' + kwargs.pop('subparser')](**kwargs)
            case 'init':
                if backup.is_backup_dir():
                    print("alredy initialized")
                else:
                    globals()['backup' + kwargs.pop('subparser')](**kwargs)
            case 'clone':
                globals()['backup' + kwargs.pop('subparser')](**kwargs)
            case _:
                parser.print_help(sys.stderr)

    # globals()[kwargs.pop('subparser')](**kwargs)
