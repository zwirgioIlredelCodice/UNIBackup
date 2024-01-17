# Indice
**[Come funziona](#come_funziona)**<br>
**[Lessico](#lessico)**<br>
**[Utilizzo](#utilizzo)**<br>
**[Best practices](best_practices)**<br>
**[Errori e warnings](#errori_e_warnings)**<br>


<a id="lessico"></a>

# Lessico

* __unibackup directory__ è una cartella propriamente inizializzata per essere usata con __unibackup__, l'equivalente di una cartella (repository di git) inizializzata con `git init .`
* __local__ è una __unibackup directory__ presente nel disco del proprio pc
* __remote__ è una __unibackup directory__ presente nei server di OneDrive


<a id="come_funziona"></a>

# Come funziona

Unibackup è fodamentalmente un wrapper per [rclone](https://rclone.org/), quindi per ogni comando di unibackup corrispondono uno o più comandi di rclone, questi comandi vengono eseguiti come processi figli da unibackup tramite la funzione `shell` in `src/module/ulility.py`.


## file di UNIBackup

questi file vengono creati all'inizializzata di una cartella con unibackup, ovvero si devono trovare in un __unibackup directory__ per renderla tale.

* `.unibackup` file creato con al suo interno impostazioni di unibackup usate tra dispositivi differenti, ha anche lo scopo di identificare che è una cartella inizializzata da unibackup

* `.unibackup_local` file con al suo interno impostazioni non utilizzabili tra dispositivi diversi

* `.unibackup_ignore` file con regole di esclusione/inclusione di file dai backups la sintassi di questo file è spiengata nella [documentazione di rclone --files-from](https://rclone.org/filtering/#filter-from-read-filtering-patterns-from-a-file)


<a id="utilizzo"></a>

# Utilizzo

i sono simili a quelli di git sia per la sintassi che per quello che fanno

```
usage: unibackup.py [-h]
                    {status,config,init,listbackups,clone,deletebackup,safepush,safepull,push,pull,sync,rclone}
                    ...

positional arguments:
  {status,config,init,listbackups,clone,deletebackup,safepush,safepull,push,pull,sync,rclone}
    status              Show the working tree status
    config              configure unibackup
    init                initialize an exisiting directory as a unibackup
                        direcory
    listbackups         list all unibackup direcory remotly saved
    clone               clone a unibackup direcory into a new directory
    deletebackup        delete a remotly saved unibackup directory
    safepush            sync remote with local without deleting files in
                        remote
    safepull            sync local with remote without deleting files in local
    push                sync remote with local
    pull                sync local with remote
    sync                perform bidirectional synchronization between local
                        and remote
    rclone              call rclone with argument provided, replce LOCAL and
                        REMOTE with unibackup equivalent path

options:
  -h, --help            show this help message and exit
```

## inizializzata

### config

```
unibackup config
```

Aggancia __rclone__ al drive di OneDrive.
Quando viene eseguito questo comando si aprirà una pagine web di login di OneDrive dove bisogna accedere e dare i permessi necessari, per gli studenti accedere con la mail istituzionale es. `nome.cognome@studio.unibo.it`, se non si apre la pagina web copiare ed incollare il link che appare sul terminale in un browser web

### init

```bash
unibackup init
```

fa diventare la cartella in cui viene eseguito una __unibackup directory__, la cartella può essere anche piena

esempio
```bash
mkdir appunti-da-salvare
cd appunti-da-salvare

unibackup init
```

### clone

```bash
unibackup.py clone -d REMOTE_DIR
```

clona una __remote__ nella cartella dove viene eseguito il comando, `REMOTE_DIR` è il nome della __remote__ da clonare

esempio

guardo la lista di __remote__ disponibili
```bash
unibackup listbackups
```
output
```
 rclone listremotes
 rclone lsjson unibackup:unibackup/current/
list of folders saved in remote:
appunti-da-salvare
```

clono `appunti-da-salvare`

```bash
unibackup clone -d appunti-da-salvare
```

### deletebackup

```bash
unibackup.py deletebackup -d REMOTE_DIR
```

cancella una __remote__ nella cartella dove viene eseguito il comando, `REMOTE_DIR` è il nome della __remote__ da cancellare

## informazioni

### status

```bash
unibackup status
```

fa vedere lo stato della __unibackup directory__ in cui viene eseguito,
ovvero fa vedere quali file sono stati aggiunti/cancellati/cambiati in __local__ rispetto a __remote__

### listbackups

```bash
unibackup listbackups
```

fa vedere la lista di __unibackup directory__ salvate in OneDrive

## sincronizzazione


### safepush

```bash
unibackup safepush
```

aggiorna il contenuto di __remote__ rispetto alla __unibackup directory__
in cui viene eseguito, __i file cancellati in local non vengono cancellati in remote__

### push

```bash
unibackup push
```

aggiorna il contenuto di __remote__ rispetto alla __unibackup directory__
in cui viene eseguito,

### safepull

```bash
unibackup safepull
```

aggiorna il contenuto della __unibackup directory__
in cui viene eseguito rispetto a __remote__, __i file cancellati in remote non vengono cancellati in local__

### pull

```bash
unibackup pull
```

aggiorna il contenuto della __unibackup directory__
in cui viene eseguito rispetto a __remote__


### sync

```bash
unibackup sync
```

aggiorna __local__ e __remote__ dell'__unibackup directory__ in cui viene eseguito prendendo le versioni dei file più nuove da entrambe.  
__usa deli comandi sperimentali, usare a priprio rischio e pericolo__

Questo comando può tornare utile quando ci sono nouve versioni di file sia in __local__ che in __remote__


## interfacciarsi con rclone

```bash
unibackup rclone RCLONE_COMMAND
```

chiama __rclone__ con i comandi `RCLONE_COMMAND`, [lista di comandi di rclone](https://rclone.org/commands/)

unibackup sostituisce i seguenti termini in `RCLONE_COMMAND`_

* sostituisce __REMOTE__ con la path di __remote__ della __unibackup directory__ in cui viene eseguito
* sostituisce __LOCAL__ con la path di __local__ della __unibackup directory__ in cui viene eseguito

### esempi

clona `appunti-da-salvare` lista tutte le cartelle in `appunti-da-salvare` nel cloud e quelle in locale
```bash
unibackup clone -d appunti-da-salvare
cd appunti-da-salvare

unibackup rclone lsd REMOTE # it runs rclone lsd unibackup:unibackup/current/appunti-da-salvare
unibackup rclone lsd LOCAL  # it runs rclone lsd /home/fabio/appunti-da-salvare
```


<a id="best_practices"></a>

# Best practices

* questo programma è stato creato per fare backups di appunti e materiale didattico quindi sconsigia di fare backups di cartelle contenenti
artfatti di compilazione, cartelle .git ed altre cartelle con tantissimi file di poca importanza per non incappare in problematiche. Questi
file si possono escludere tramite il file `.unibackup_ignore`.
* Si consigia di mantenere il numero di file di un backup inferiore ai 5000, in quanto quando si vanno a spostare grandi numeri di file
Onedrive limita la velocità di trasperimento fino a bloccarla completamente, in questo caso si può interrompere il programma e rieseguirlo
dopo alcuni minuti, il trasferimento riparterà da dove interrotto.

<a id="errori_e_warnings"></a>

# Errori e warnings

* se rclone ha problemi ad accedere perchè Onedrive gli ha revocato i permessi rieseguire la configurazione con `unibackup config`

* in molte occasioni rclone da errori che non compromettono il funzionamento e quindi possono essere ignorati come ad esempio con l'eseguzione di `unibackup status` in output `'ERROR : file.txt: file not in OneDrive root 'unibackup/current/myfolder'` (quando `myfile.txt` è presente solo il __remote__ e non in __local__ e viceversa)
