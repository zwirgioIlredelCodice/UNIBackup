#!/usr/bin/env python3
import os

import module.rclone
import module.backup


if __name__ == "__main__":
    cwd = os.getcwd()

    import sys
    if len(sys.argv) <= 1:
        print("help ...")
        exit()

    args = sys.argv[1:]
    command = args[0]

    if command == 'info':
        print("rclone version:", module.rclone.version())
    elif command == 'status':
        print("active:", module.backup.is_backup_dir(cwd))
    else:
        print("help ...")
