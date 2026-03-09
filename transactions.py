"""
P2PKH and P2SH-segwit workflow.
"""

import json

import config as c
from utils.rpc import BitcoinRPC
from utils.utxo import normalize_utxos
from utils.converters import sat_to_btc, btc_to_sat
from utils.tx import pretty_format, select_utxos, build_inputs, build_outputs
from utils.addresses import save_addresses, load_addresses

def transfer_funds(from_addr, to_addr, amount, fee_rate, rpc, is_witness, atob):
    utxos = normalize_utxos(rpc.list_unspent([from_addr]))

    if not atob:
        print("INFO: listunspent for B")
        print(utxos)
        print("INFO: txid for UTXO of B:", utxos[0]["txid"])

    print(f"INFO: Creating raw_tx ({sat_to_btc(amount)} BTC)")
    selected, change, fee = select_utxos(utxos, amount, to_addr, from_addr, fee_rate, rpc, is_witness)
    print(f"INFO: Calculated fee: {fee} sat")
    inputs = build_inputs(selected)
    outputs = build_outputs(to_addr, amount, from_addr, change)
    raw_tx = rpc.create_raw_tx(inputs, outputs)

    print("INFO: Signing tx")
    signed = rpc.sign_raw_tx(raw_tx)

    print("INFO: Broadcasting tx")
    txid = rpc.broadcast_tx(signed["hex"])

    print("INFO: Decoding signed tx")
    decoded_tx = rpc.decoderawtransaction(signed["hex"], is_witness=is_witness)
    print(pretty_format(decoded_tx))
    if atob:
        print("INFO: scriptPubKey:", decoded_tx["vout"][0]["scriptPubKey"]["asm"], sep="\n")
    elif not atob:
        print("INFO: scrictSig:", decoded_tx["vin"][0]["scriptSig"]["asm"], sep="\n")

    print("INFO: txid", txid)
    # mine to confirm the transaction
    rpc.mine(1)

def run_tx_flow(type, stage):
    rpc = BitcoinRPC()
    rpc.mine()
    if type == "p2pkh":
        addr_type = "legacy"
        is_witness = False
    elif type == "p2sh-segwit":
        addr_type = "p2sh-segwit"
        is_witness = True
    else:
        raise ValueError(f"Invalid transaction flow type: {type}")

    print("INFO: Addresses")
    if stage == "AtoB":
        A = rpc.get_new_address(addr_type)
        B = rpc.get_new_address(addr_type)
        C = rpc.get_new_address(addr_type)
        save_addresses(A, B, C, addr_type)
    elif stage == "BtoC":
        A, B, C = load_addresses(addr_type)
    if stage == "AtoB":
        print("A:", A)
    print("B:", B)
    if stage == "BtoC":
        print("C:", C)

    if stage == "AtoB":
        print(f"INFO: Funding A ({sat_to_btc(c.DEFAULT_FUND_A)} BTC)")
        rpc.send_to_address(A, c.DEFAULT_FUND_A)
        print("-"*20 + " A -> B " + "-"*20)
        transfer_funds(A, B, c.DEFAULT_TX_A_TO_B, c.DEFAULT_FEE_RATE, rpc, is_witness, True)
    elif stage == "BtoC":
        print("-"*20 + " B -> C " + "-"*20)
        transfer_funds(B, C, c.DEFAULT_TX_B_TO_C, c.DEFAULT_FEE_RATE, rpc, is_witness, False)
