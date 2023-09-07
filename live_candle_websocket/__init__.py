from commons.commons import pairs, config, intervals

LIVE_CANDLE = "live_candle"
server_url = config[LIVE_CANDLE]["server_url"]
server_port = config[LIVE_CANDLE]["server_port"]
binance_url = config[LIVE_CANDLE]["binance_url"]

cache_keys = {}
binance_keys = []


def binance_naming(pair, interval):
    return f"{pair.lower()}@kline_{interval}"


def cache_naming(pair, interval):
    return f"ws_lc_{pair}_{interval}"


def generate_keys():
    for pair in pairs:
        candle_pair_cache_keys = {}
        for interval in intervals:
            binance_keys.append(binance_naming(pair, interval))
            candle_pair_cache_keys[interval] = cache_naming(pair, interval)
        cache_keys[pair] = candle_pair_cache_keys


def __init():
    generate_keys()
    print(cache_keys)
    print(binance_keys)

__init()
