import yaml

INTERVAL_INDEX = 0
CACHE_KEY_INDEX = 1
BINANCE_KEY_INDEX = 2


def cache_naming(pair, interval):
    return f"ws_lc_{pair}_{interval}"


try:
    with open('pairs.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    pairs = config['pairs']
    intervals = config['intervals']
    binance_url = config['binance_url']
    redis_port = config['redis_port']
    redis_host = config['redis_host']
    websocket_port = config['websocket_port']
    websocket_url = config['websocket_url']

    pair_keys_map = {
        pair: [(interval, cache_naming(pair, interval), f"{pair.lower()}@kline_{interval}") for interval in
               intervals]
        for pair in pairs
    }
except Exception as e:
    print(e)
    exit(-1)
