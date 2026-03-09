import json
from decimal import Decimal

from utils.converters import sat_to_btc, btc_to_sat

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def pretty_format(tx):
    return json.dumps(tx, indent=4, cls=DecimalEncoder)

def select_utxos(utxos, send_sats, dest_addr, change_addr, fee_rate, rpc, is_witness):
    """
    Select UTXOs using exact transaction size feedback.
    """

    utxos = sorted(utxos, key=lambda u: u["amount_sats"])

    selected = []
    total = 0
    fee = 0

    for u in utxos:
        selected.append(u)
        total += u["amount_sats"]

        while True:
            change = total - send_sats - fee
            outputs = {dest_addr: sat_to_btc(send_sats)}

            if change > 0:
                outputs[change_addr] = sat_to_btc(change)

            inputs = build_inputs(selected)

            raw = rpc.create_raw_tx(inputs, outputs)
            signed = rpc.sign_raw_tx(raw)
            decoded = rpc.decoderawtransaction(signed["hex"])

            vsize = decoded["vsize"]
            new_fee = vsize * fee_rate

            if new_fee == fee:
                return selected, change, fee
            fee = new_fee

            if total < send_sats + fee:
                break

    raise ValueError("Insufficient UTXOs")

def build_inputs(selected):
    """
    Convert selected UTXOs to createrawtransaction input format.
    """

    return [{"txid": u["txid"], "vout": u["vout"]} for u in selected]


def build_outputs(dest_addr, send_sats, change_addr, change_sats):
    """
    Build outputs dictionary.
    """

    outputs = {
        dest_addr: sat_to_btc(send_sats)
    }

    if change_sats:
        outputs[change_addr] = sat_to_btc(change_sats)

    return outputs
