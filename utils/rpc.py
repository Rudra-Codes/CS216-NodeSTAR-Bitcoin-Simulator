"""
RPC wrapper using python-bitcoinlib.
"""

from bitcoin import SelectParams
from bitcoin.rpc import Proxy, JSONRPCError
import config as c


class BitcoinRPC:
    """
    Simple wrapper around bitcoin.rpc.Proxy.
    """

    def __init__(self):
        SelectParams('regtest')
        try:
            self.rpc = Proxy(service_url=f"http://{c.RPC_USER}:{c.RPC_PASSWORD}@{c.RPC_HOST}:{c.RPC_PORT}/wallet/{c.WALLET_NAME}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to bitcoind: {e}")
        try:
            self.rpc._call('loadwallet', f"{c.WALLET_NAME}", False)
        except JSONRPCError as e:
            code = e.error.get("code")
            if code == -35:
                pass
            elif code == -18:
                self.rpc._call('createwallet', f"{c.WALLET_NAME}")
            else:
                raise e

    def get_new_address(self, addr_type="legacy"):
        return str(self.rpc._call("getnewaddress", "", addr_type))

    def mine(self, cnt=101):
        addr = self.get_new_address()
        self.rpc.generatetoaddress(cnt, addr)

    def send_to_address(self, address, amount_sat):
        """Load an address """
        try:
            return self.rpc.sendtoaddress(address, amount_sat)
        except JSONRPCError as e:
            if e.error.get("code") == -6:
                print("INFO: Insufficient funds in wallet; Mining")
                self.mine()
                return self.send_to_address(address, amount_sat)
            raise

    def list_unspent(self, addrs=None):
        return self.rpc.listunspent(minconf=0, addrs=addrs)

    def create_raw_tx(self, inputs, outputs):
        return self.rpc._call("createrawtransaction", inputs, outputs)

    def sign_raw_tx(self, raw_tx):
        return self.rpc._call("signrawtransactionwithwallet", raw_tx)

    def broadcast_tx(self, hex_tx):
        return self.rpc._call("sendrawtransaction", hex_tx, 0)

    def decoderawtransaction(self, raw_tx, is_witness=None):
        if is_witness is not None:
            return self.rpc._call("decoderawtransaction", raw_tx, is_witness)
        return self.rpc._call("decoderawtransaction", raw_tx)
