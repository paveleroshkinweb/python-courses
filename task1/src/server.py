import logging
from sockets.server_socket import ServerSocket
from utils.parse_cli_params import get_server_config
import signal


if __name__ == '__main__':
    logging.basicConfig(level='INFO', format='%(asctime)s - %(levelname)s - %(message)s')
    server_config = get_server_config()
    server_socket = ServerSocket(server_config)
    signal.signal(signal.SIGINT, lambda sig, frame: server_socket.exit('Clothing server ...', 1))
    server_socket.start()
