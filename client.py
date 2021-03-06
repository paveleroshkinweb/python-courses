from src.sockets.client_socket import ClientSocket
from src.utils.parse_cli_params import get_client_config
import logging
import signal


if __name__ == '__main__':
    logging.basicConfig(level='INFO', format='%(asctime)s - %(message)s')
    client_config = get_client_config()
    client_socket = ClientSocket(client_config)
    signal.signal(signal.SIGINT, lambda sig, frame: client_socket.exit('Closing client ...', 1))
    client_socket.start()
