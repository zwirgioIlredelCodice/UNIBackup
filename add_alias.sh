FILE='src/unibackup.py'
BPATH="$(pwd)/$FILE"
COMMAND="python3 $BPATH"
UNIBACKUP_ALIAS="alias unibackup='$COMMAND'"

# check if is already defined
if cat $HOME/.bashrc | grep -q 'alias unibackup='; then
    echo 'already added'
else

    if [ -f $FILE ]; then

        echo 'added alias:'
        echo $UNIBACKUP_ALIAS

        echo '# alias for unibackup' >> $HOME/.bashrc
        echo $UNIBACKUP_ALIAS >> $HOME/.bashrc
        printf '\nclose and reopen the terminal use unibackup as a command\n'
    else
        echo 'run this script in the UNIBackup direcotory'
    fi
fi
