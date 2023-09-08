import threading
from tick_data_websocket.tick_data_websocket_api import websocket_server_process as tick_data_websocket_server_process
from live_candle_websocket.live_candle_websocket_api import websocket_server_process as live_candle_websocket_server_process


if __name__ == "__main__":
    tick_data_websocket_thread = threading.Thread(target=tick_data_websocket_server_process)
    live_candle_websocket_thread = threading.Thread(target=live_candle_websocket_server_process)

    tick_data_websocket_thread.start()
    live_candle_websocket_thread.start()

    tick_data_websocket_thread.join()
    live_candle_websocket_thread.join()
    while True:
        pass