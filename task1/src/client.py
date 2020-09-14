from sockets.client_socket import ClientSocket
from utils.parse_cli_params import get_client_config
import logging


if __name__ == '__main__':
    logging.basicConfig(level='INFO', format='%(asctime)s - %(message)s')
    client_config = get_client_config()
    client_socket = ClientSocket(client_config)
    client_socket.start()
