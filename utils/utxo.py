"""
UTXO helper utilities
"""

from bitcoin.core import b2lx

def normalize_utxo(utxo):
    """
    Convert Proxy() listunspent result into a simple dict.
    """

    outpoint = utxo["outpoint"]

    return {
        "txid": b2lx(outpoint.hash),
        "vout": outpoint.n,
        "outpoint": outpoint,
        "scriptPubKey": utxo["scriptPubKey"],
        "amount_sats": int(utxo["amount"]),
        "confirmations": utxo.get("confirmations", 0),
        "address": str(utxo.get("address", "")),
    }


def normalize_utxos(utxos):
    return [normalize_utxo(u) for u in utxos]
