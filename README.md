# Bitcoin Transaction Simulator

## Typical dev workflow:
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ensure bitcoind running in regtest mode
# (for non-default setups, configure parameters in config.py)
python main.py
```

## Synopsis
```shell
$ python main.py -h
usage: main.py [-h] [--type {legacy,p2sh-segwit,both}] [--stage {AtoB,BtoC,both}]

options:
  -h, --help            show this help message and exit
  --type {legacy,p2sh-segwit,both} # default: both
  --stage {AtoB,BtoC,both}         # default: both
```
