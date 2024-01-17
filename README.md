# UNIBackup

Backups and mantain files up to date between devices


## About The Project

### features

* can save files on __onedrive__ unibo students account whic has 2TB of capacity
* syntax similar to git
* backups files
* sync files across devices

## Getting Started

### Prerequisites

* have a onedrive account, for unibo students eg. `name.surname@studio.unibo.it`
* have installed these program:
    * `git`
    * `python3`
    * `rclone`
    * `bash` *optional but recomended*


### Installation

1. clone this proget repository in a folder you want
    * run `git clone https://github.com/zwirgioIlredelCodice/UNIBackup.git`
2. open a terminal in the repo directory and run the "installation" script that add unibackup as an alias in the `.bashrc` files
    * run `bash add_alias.sh`

Now you can run `unibackup` as a command in the terminal.
If you do't want/cant run the bash script you can run this program with `python3 {path_to_UNIBackup_repo/src/unibackup.py}`


### Update

1. open a terminal in the repo directory and run the "installation" script that add unibackup as an alias in the `.bashrc` files
    * run `git pull`


## Usage

in the terminal

```bash
$ unibackup
```

* see `unibackup --help` for helps
* __for get started tutorial see the [tutoral](TUTORIAL.md)__
* __for an in depth look see the [documentation](DOCUMENTATION.md) file__


## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the GPLv3 License. See `LICENSE.txt` for more information.


## Contact

Fabio Murer - fabio.murer@studio.unibo.it

Project Link: [https://github.com/zwirgioIlredelCodice/UNIBackup](https://github.com/zwirgioIlredelCodice/UNIBackup)


## Acknowledgments

* [rclone](https://rclone.org/)

