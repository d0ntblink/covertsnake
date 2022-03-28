# covertsnake
## Gary. K and Amir. Z
### 3/27/2022


[Github Link](https://github.com/d0ntblink/covertsnake)

## Requirements

**This program is only tested on a linux enviorment**

**This program requires root access**

### Required Programs

* Python3
* pip

### Required Python Libraries

* scapy
* sys
* os
* tqdm
* logging
* base64

## Setup:

```
## install python and pip
apt install python3 python3-pip

## install required python libs
pip install tqdm scapy

## download gutenzahler
git clone https://github.com/d0ntblink/covertsnake
cd coversnake/Code
chmod +x covertsnake.py
```

## Usage:
to run the program in server mode
`covertsnake.py --server`

to run the program in client mode

`covertsnake.py --client --ip <server ip> --file <file name to transfer>`

to run the program in debug mode

`covertsnake.py --debug --server`

***NOTE: --debug must be the first argument***

## Arguments:
- --help: displays this message
- --ip: server ip
- --file: the name of the file you want to transfer
- --server: runs the program in server mode
- --client: runs the program in client mode
- --debug: enables debug mode must be the first argument

## Example:
`sudo covertsnake.py --server`

`sudo covertsnake.py --client --file example.pdf --ip 10.0.0.245`