import asyncio
import json
import websockets
import time
import redis
import threading
from commons import pairs, binance_url, redis_host, redis_port, websocket_url, websocket_port
import websocket


def on_message(ws, message):
    candle_data = json.loads(message)
    timestamp = time.time()
    # Format response
    try:
        if candle_data["e"] == "kline":
            candlestick = candle_data["k"]
            label = candlestick["s"]+candlestick["i"]
            data = json.dumps(candle_data)
            redis_cache.zadd(label, {data: timestamp})  # Add received data to redis
    except Exception as e:
        print(e)


def on_error(ws, error):
    print("WebSocket Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")


def on_open(ws):
    payload = {
        "method": "SUBSCRIBE",
        "params": pairs,
        "id": 1
    }
    ws.send(json.dumps(payload))  # Connect Binance socket
    print("WebSocket Opened")


def get_last_data(label):
    current_timestamp = time.time()
    data = redis_cache.zrangebyscore(label, '-inf', current_timestamp)  # Get timestamped datas from redis
    data_str = data[-1].decode('utf-8')  # Get last timestamped data
    return data_str


async def echo(ws, path):
    global last_data
    if_open = True
    parts = path.lstrip('/').split('@')
    while if_open:
        try:
            label = parts[0]+parts[1]
            candle_data = get_last_data(label)
            last_data = candle_data
            if candle_data:
                await ws.send(candle_data)
                await asyncio.sleep(1)
            else:
                await ws.send(last_data)
        except websockets.exceptions.ConnectionClosed:
            if_open = False
            # The WebSocket connection has been closed by the client
            print("WebSocket connection closed by client")
        except Exception as e:
            print(e)


def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(echo, websocket_url, websocket_port)
    loop.run_until_complete(start_server)
    loop.run_forever()


def start_websocket_listener():
    ws = websocket.WebSocketApp(binance_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    # Create and start a separate thread for the WebSocket listener
    redis_cache = redis.Redis(host=redis_host, port=redis_port)
    websocket_thread = threading.Thread(target=start_websocket_server)
    client_thread = threading.Thread(target=start_websocket_listener)
    client_thread.start()
    websocket_thread.start()
    while True:
        # Your main thread logic here
        websocket_thread.join()  # This should work as expected now
        client_thread.join()
        pass