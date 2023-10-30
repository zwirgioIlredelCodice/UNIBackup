#!/usr/bin/env python3
import os

import module.rclone as rclone
import module.backup as backup


if __name__ == "__main__":
    cwd = os.getcwd()

    if not backup.is_configured():
        # TODO: better error
        print("unibackup is not configured,\n\trun ...")
        exit()
    if not backup.is_backup_dir(cwd):
        # TODO: better error
        print("unibackup is not initialize in this directory,\n\trun ...")
        exit()

    import sys
    if len(sys.argv) <= 1:
        print("help ...")
        exit()

    args = sys.argv[1:]
    command = args[0]

    if command == 'info':
        print("rclone version:", rclone.version())
    elif command == 'status':
        print("active:", backup.is_backup_dir(cwd))
    else:
        print("help ...")
