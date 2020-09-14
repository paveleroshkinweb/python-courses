from models.server_socket import ServerSocket
from utils.parse_cli_params import get_server_config


if __name__ == '__main__':
    server_config = get_server_config()
    server_socket = ServerSocket(server_config)
    server_socket.start()
