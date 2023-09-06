import redis
import yaml

INTERVAL_INDEX = 0
CACHE_KEY_INDEX = 1
BINANCE_KEY_INDEX = 2


def candle_binance_key_naming(pair, interval):
    return f"{pair.lower()}@kline_{interval}"


def tick_data_binance_key_naming(pair):
    return f"{pair.lower()}@ticker"


def candle_cache_naming(pair, interval):
    return f"ws_lc_{pair}_{interval}"


def tick_data_cache_naming(pair):
    return f"ws_td_{pair}"

#
# def generate_candle_keys(pairs, intervals):
#     return {pair: {interval: candle_cache_naming(pair, interval) for interval in intervals} for pair in pairs}


try:
    with open('config.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    pairs = config['pairs']
    intervals = config['intervals']
    redis_port = config['redis_port']
    redis_host = config['redis_host']

    binance_kline_url = config['binance_kline_url']
    candle_websocket_port = config['candle_websocket_port']
    candle_websocket_url = config['candle_websocket_url']

    binance_tick_url = config["binance_tick_url"]
    tick_data_websocket_port = config["tick_data_port"]
    tick_data_websocket_url = config["tick_data_url"]

    candle_binance_keys = []
    tick_data_binance_keys = []
    candle_cache_keys = {}
    tick_data_cache_keys = {}

    for pair in pairs:
        tick_data_binance_keys.append(tick_data_binance_key_naming(pair))
        tick_data_cache_keys[pair] = tick_data_cache_naming(pair)

        candle_pair_cache_keys = {}
        for interval in intervals:
            candle_binance_keys.append(candle_binance_key_naming(pair, interval))
            candle_pair_cache_keys[interval] = candle_cache_naming(pair, interval)
        candle_cache_keys[pair] = candle_pair_cache_keys

    print(candle_binance_keys)
    print(tick_data_binance_keys)
    print(candle_cache_keys)
    print(tick_data_cache_keys)

    cache_process = redis.Redis(host=redis_host, port=redis_port)

except Exception as e:
    print(e)
    exit(-1)
