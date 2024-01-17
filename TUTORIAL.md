# Tutorial pratico di UNIbackup

## Setup

1. eseguire l'installazione di UNIbackup come descritto nel [README](README.md)
2. eseguire la configurazione di UNIbackup eseguendo `unibackup config` nel terminale, inserire email e password dell'ateneo se richieste.

## Creazione di backups

1. creo una nuova cartella `appunti` in `Documents` e creo il file `ciao.txt`

    ```bash
    cd ~/Documets
    mkdir appunti
    cd appunti
    touch ciao.txt
    ```

2. inizializzo la cartella `appunti` ad una **unibackup directory**

    ```bash
    unibackup init
    ```

se si vuole utilizzare una cartella già creata saltare il primo passaggio e eseguire `unibackup init` all'interno di quella cartella

## Salvataggio e ripristino

1. salvo su OneDrive il backup precedentemente creato
    ```bash
    unibackup safepush
    ```
2. simulo una perdita dei dati cancellando la cartella
    ```bash
    cd ..
    rm -rf appunti
    ```
3. ripristino i dati
    ```bash
    unibackup clone -d appunti
    cd appunti
    ls
    ```

    i file sono stati ripristinati


## Si può fare molto di più...

per la spiegazione di tutti i comandi disponibili leggere [DOCUMENTATION](DOCUMENTATION.md)
