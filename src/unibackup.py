#!/usr/bin/env python3
import os
import sys
import argparse

from module.backup import Backup
from module.utility import prettyPrint, shell


if __name__ == "__main__":
    cwd = os.getcwd()
    backup = Backup(cwd)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    status_parser = subparsers.add_parser(
        'status',
        help='Show the working tree status')

    config_parser = subparsers.add_parser(
        'config',
        help='configure unibackup')

    init_parser = subparsers.add_parser(
        'init',
        help='initialize an exisiting directory as a unibackup direcory')

    listbackups_parser = subparsers.add_parser(
        'listbackups',
        help='list all unibackup direcory remotly saved')

    clone_parser = subparsers.add_parser(
        'clone',
        help='clone a unibackup direcory into a new directory')
    clone_parser.add_argument(
        '-d',
        dest='remote_dir',
        help='direcory name to clone')

    deletebackup_parser = subparsers.add_parser(
        'deletebackup',
        help='delete a remotly saved unibackup directory')
    deletebackup_parser.add_argument(
        '-d',
        dest='remote_dir',
        help='direcory name to delete')

    safepush_parser = subparsers.add_parser(
        'safepush',
        help="sync remote with local without deleting files in remote")

    safepull_parser = subparsers.add_parser(
        'safepull',
        help="sync local with remote without deleting files in local")

    push_parser = subparsers.add_parser(
        'push',
        help="sync remote with local")

    pull_parser = subparsers.add_parser(
        'pull',
        help="sync local with remote")

    sync_parser = subparsers.add_parser(
        'sync',
        help="perform bidirectional synchronization between local and remote")

    rclone_parser = subparsers.add_parser(
        'rclone',
        help="call rclone with argument provided, replce LOCAL and REMOTE with unibackup equivalent path")

    if len(sys.argv) > 1 and sys.argv[1] == 'rclone':
        subcommand = 'rclone'
    else:
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
                    backup.sync(**kwargs)
    else:
        match subcommand:
            case 'config':
                backup.config(**kwargs)
            case 'listbackups':
                backup.listbackups()
            case 'init':
                if backup.is_backup_dir():
                    prettyPrint.warn("alredy initialized")
                else:
                    backup.init(**kwargs)
            case 'clone':
                backup.clone(**kwargs)
            case 'deletebackup':
                backup.deletebackup(**kwargs)
            case 'rclone':
                topass = sys.argv[1:]
                for i in range(len(topass)):
                    if topass[i] == 'LOCAL':
                        topass[i] = backup.local
                    elif topass[i] == 'REMOTE':
                        topass[i] = backup.remote
                shell(topass)
            case _:
                parser.print_help(sys.stderr)
