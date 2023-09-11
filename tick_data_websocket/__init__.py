from commons.commons import pairs, config

TICK_DATA = "tick_data"
server_url = config[TICK_DATA]["server_url"]
server_port = config[TICK_DATA]["server_port"]
binance_url = config[TICK_DATA]["binance_url"]


cache_keys = {}
binance_keys = []


def binance_naming(pair):
    return f"{pair.lower()}@ticker_1h"


def cache_naming(pair):
    return f"ws_td_{pair}"


def generate_keys():
    for pair in pairs:
        binance_keys.append(binance_naming(pair))
        cache_keys[pair] = cache_naming(pair)


def __init():
    generate_keys()


__init()
