import threading
import logging
from server.server import ThreadedTCPRequestHandler, ThreadedTCPServer

"""
This is the main file for the server
"""

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 1234
    logging.basicConfig(
        filename='server_data/logs/server.log',
        level=logging.DEBUG,
        format='[%(asctime)s] %(message)s'
    )
    logging.info(f'Server listening on {HOST}:{PORT}')

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        while True:
            pass
        server.shutdown()
