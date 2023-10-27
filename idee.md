# Idee per csuniBackup

## cosa deve essere
uno script/programma che effettua il backup di file su **onedrive** (gli studenti unibo hanno a disposizone onedrive gratuito senza limiti di spazio)

## stato di sviluppo
* trovato un modo per caricare/scaricare file da onedrive con **rclone**

## idee

* creare uno script che confugura **rclone** e che faccia il synch di una cartella (pull push da onedrive)

## da fare

- [ ] creare lo script
- [ ] crare interfaccia grafica
- [ ] metterlo su github

## siti utili

* [https://medium.com/swlh/using-rclone-on-linux-to-automate-backups-to-google-drive-d599b49c42e8]
* [https://rclone.org/docs/]
* [https://github.com/Johannes11833/rclone_python]


## script

# funzionamento

* **config**
    * setup di rclone con cartelle `unibackup`
* **init** da fare nella cartella da salvare
    * crea file `.unibackup.json` con tutte le informazioni per lo script
    * crea il file `.unibackupugnore` con tutte le opzioni di cartelle/file da ignorare durante clone/upload/downolad
* **clone cartella** da fare dove vuoi che venga scaricata la cattella salvata
    * copia la cartella da remote a dove viene eseguito (la cartella è pronta per essere usata da unibackup
* **upload**
    * effettua il sync su remote della cartella
* **sync**
    * effettua il bisync della cartella
