# Bitcoin Transaction Simulator

This repository contains the implementation and solution for the **CS 216: Bitcoin Transaction Lab assignment**.

## Prerequisites

- **Bitcoin Core (`bitcoind`)**: Must be installed and configured on your system.
- **Python 3**: Ensure Python 3 and `pip` are installed.

### Bitcoin Configuration

Before starting `bitcoind`, configure your `bitcoin.conf` file with the following settings:

```ini
# Run in regression test mode
regtest=1
# Enable server mode for RPC
server=1
rest=1
# RPC authentication
rpcuser=rpcuser
rpcpassword=rpcpassword
# Wallet settings
paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
```
Make corresponding configuration change in `config.py` if your `bitcoin.conf` differs.
Start `bitcoind`:

```shell
bitcoind
```
## How to run guide:
Use this for running both stages (A -> B and B -> C) for both P2PKH and P2SH-SegWit:
```shell
# optional (recommended): use a virtual environment
python -m venv .venv
source .venv/bin/activate # Linux
# install dependencies
pip install -r requirements.txt

python main.py
```

## Command Synopsis
The program supports running different stages and types of the simulator using the following command line arguments:
```shell
$ python main.py -h
usage: main.py [-h] [--type {legacy,p2sh-segwit,both}] [--stage {AtoB,BtoC,both}]

options:
  -h, --help            show this help message and exit
  --type {legacy,p2sh-segwit,both} # default: both
  --stage {AtoB,BtoC,both}         # default: both
```

## Assignment Features
It performs the following:
- **Part 1:** Legacy Address Transactions (P2PKH) flow (A -> B -> C)
- **Part 2:** P2SH-SegWit Address Transactions flow (A' -> B' -> C')

## Team Members
- **Rudra Chitkara** (Roll Number: 240041031)
- **Aayush** (Roll Number: 240041001)
- **Tanish Yadav** (Roll Number: 240041036)
- **Siddh Nema** (Roll Number: 240002070)

