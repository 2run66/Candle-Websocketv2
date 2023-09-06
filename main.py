# import threading
#
# if __name__ == "__main__":
#     # Create and start a separate thread for the WebSocket listener
#
#     websocket_thread = threading.Thread(target=websocket_server_process)
#     binance_client_thread = threading.Thread(target=binance_websocket_subscriber_process)
#     binance_client_thread.start()
#     websocket_thread.start()
#     while True:
#         # Your main thread logic here
#         websocket_thread.join()  # This should work as expected now
#         binance_client_thread.join()
#         pass