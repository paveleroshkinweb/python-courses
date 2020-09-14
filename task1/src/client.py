from models.client_socket import ClientSocket
from utils.parse_cli_params import get_client_config


if __name__ == '__main__':
    client_config = get_client_config()
    client_socket = ClientSocket(client_config)
    client_socket.start()
