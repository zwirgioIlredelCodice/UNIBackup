#!/usr/bin/env python3
import os
import sys
import argparse

import module.rclone as rclone
from module.backup import Backup
from module.utility import prettyPrint


if __name__ == "__main__":
    cwd = os.getcwd()
    backup = Backup(cwd)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    status_parser = subparsers.add_parser('status',
                                          help='show the status of the running direcory')
    config_parser = subparsers.add_parser('config', help='configure unibackup')
    init_parser = subparsers.add_parser('init',
                                        help='initialize unibackup in the running direcory')

    clone_parser = subparsers.add_parser('clone',
                                        help='clone a unibackup direcory in the running direcory')
    clone_parser.add_argument('-d', '--remote_dir', dest='remote_dir',
                              help='direcory name to clone')

    push_parser = subparsers.add_parser('safepush',
                                        help="sync the remote backup with the running direcory without deleting files")
    pull_parser = subparsers.add_parser('safepull',
                                        help="sync local directory with the remote backup without deleting files")
    push_parser = subparsers.add_parser('push',
                                        help="sync the remote backup with the running direcory")
    pull_parser = subparsers.add_parser('pull',
                                        help="sync local directory with the remote backup")
    sync_parser = subparsers.add_parser('sync',
                                        help="perform bidirectional synchronization between local and remote backup")


    # https://stackoverflow.com/questions/4575747/get-selected-subcommand-with-argparse
    kwargs = vars(parser.parse_args())
    subcommand = kwargs.pop('subparser')

    if subcommand in ['status', 'safepush', 'safepull', 'push', 'pull', 'sync']:
        if not backup.is_configured():
            prettyPrint.err('unibackup is not configured')
            prettyPrint.err('run unibackup config')
        if not backup.is_backup_dir():
            prettyPrint.err('unibackup is not initialize in this directory')
            prettyPrint.err('run unibackup init')
        else:
            match subcommand:
                case 'status':
                    backup.status(**kwargs)
                case 'safepush':
                    backup.safepush(**kwargs)
                case 'safepull':
                    backup.safepull(**kwargs)
                case 'push':
                    backup.push(**kwargs)
                case 'pull':
                    backup.pull(**kwargs)
                case 'sync':
                    backup.status(**kwargs)
    else:
        match subcommand:
            case 'config':
                backup.config(**kwargs)
            case 'init':
                if backup.is_backup_dir():
                    prettyPrint.warn("alredy initialized")
                else:
                    backup.init(**kwargs)
            case 'clone':
                backup.clone(**kwargs)
            case _:
                parser.print_help(sys.stderr)

    # globals()[kwargs.pop('subparser')](**kwargs)
