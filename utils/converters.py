"""
BTC <-> satoshi converters.
"""

from bitcoin.core import COIN

SATS_PER_BTC = COIN


def btc_to_sat(btc_value: float) -> int:

    sats = int(round(btc_value * SATS_PER_BTC))

    if sats / SATS_PER_BTC != btc_value:
        raise ValueError(
            f"BTC value {btc_value} is not an exact satoshi multiple"
        )

    return sats


def sat_to_btc(sats: int) -> float:

    btc = sats / SATS_PER_BTC

    if int(btc * SATS_PER_BTC) != sats:
        # Should not really happen since python floats are double precision
        raise ValueError(
            f"Float cannot exactly represent {sats} sats"
        )

    return btc
