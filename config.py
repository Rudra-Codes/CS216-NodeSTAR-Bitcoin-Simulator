"""
Configuration.
"""

RPC_USER = "rpcuser"
RPC_PASSWORD = "rpcpassword"
RPC_HOST = "127.0.0.1"
RPC_PORT = 18443
# Wallet will be created/loaded if required
WALLET_NAME = "cs216simwallet"

# Default fee (in sat/vbyte)
DEFAULT_FEE_RATE = 10
# Default amounts (in satoshis)
DEFAULT_FUND_A = 100_000_000
DEFAULT_TX_A_TO_B = 90_000_000 # <= DEFAULT_FUND_A - DEFAULT_FEE 
DEFAULT_TX_B_TO_C = 80_000_000 # <= DEFAULT_TX_A_TO_B - DEFAULT_FEE 
