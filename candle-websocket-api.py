import asyncio
import json
import websockets
import redis
import threading
import websocket
from commons import pairs, binance_url, redis_host, redis_port, websocket_url, websocket_port,\
    pair_keys_map, cache_naming, INTERVAL_INDEX, CACHE_KEY_INDEX, BINANCE_KEY_INDEX

def on_message(ws, message):
    candle_data = json.loads(message)
    # Format response
    try:
        if candle_data["e"] == "kline":
            candlestick = candle_data["k"]
            cache_name = cache_naming(pair=candlestick["s"], interval=candlestick["i"])  # ws_lc_BTCUSDT_1m
            data = json.dumps(candle_data)
            cache_process.set(cache_name, data)  # Add received data to redis
    except Exception as e:
        print(e)


def on_error(ws, error):
    print("Binance webSocket error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Binance webSocket closed.", close_msg)


def on_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": pairs,
        "id": 1
    }
    ws.send(json.dumps(payload))  # Connect Binance socket
    print("Binance webSocket opened")


def get_cached_data():
    websocket_data = {}

    for pair, keys in pair_keys_map.items():
        pair_data = {}
        for key_tuple in keys:
            cache_key = key_tuple[CACHE_KEY_INDEX]
            cached_data = json.loads(cache_process.get(cache_key))
            if cached_data:
                interval = key_tuple[INTERVAL_INDEX]
                pair_data[interval] = cached_data
        if pair_data != {}:
            websocket_data[pair] = pair_data

    data_str = json.dumps(websocket_data)
    return data_str


async def echo(ws, path):
    if_open = True
    while if_open:
        try:
            candle_data = get_cached_data()
            if candle_data:
                await ws.send(candle_data)
                await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosed:
            if_open = False
            # The WebSocket connection has been closed by the client
            print("WebSocket connection closed by client")
        except Exception as e:
            print(e)


def websocket_server_process():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(echo, websocket_url, websocket_port)
    loop.run_until_complete(start_server)
    loop.run_forever()


def binance_websocket_subscriber_process():
    ws = websocket.WebSocketApp(binance_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    # Create and start a separate thread for the WebSocket listener
    cache_process = redis.Redis(host=redis_host, port=redis_port)
    websocket_thread = threading.Thread(target=websocket_server_process)
    binance_client_thread = threading.Thread(target=binance_websocket_subscriber_process)
    binance_client_thread.start()
    websocket_thread.start()
    while True:
        # Your main thread logic here
        websocket_thread.join()  # This should work as expected now
        binance_client_thread.join()
        pass
