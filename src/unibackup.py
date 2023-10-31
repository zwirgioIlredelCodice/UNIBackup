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

    if command == "info":
        print("rclone version:", rclone.version())
    elif command == 'status':
        print("active:", backup.is_backup_dir(cwd))

    elif command == "config":
        backup.config()
    elif command == "init":
        if backup.is_backup_dir(cwd):
            print("alredy initialized")
        else:
            backup.init(cwd)
    elif command == "clone":
        backup.clone(args[1], cwd)
    elif command == "copy":
        backup.copy(cwd)
    elif command == "push":
        backup.push(cwd)
    elif command == "pull":
        backup.pull(cwd)
    elif command == "sync":
        backup.sync(cwd)
    else:
        print("help ...")
