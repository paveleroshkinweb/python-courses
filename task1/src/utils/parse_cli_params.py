import argparse


default_config = {
    'address': 'localhost',
    'port': 15397
}


def get_client_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s_address', help='server address to connect', default=default_config['address'])
    parser.add_argument('-s_port', help='server port to connect', default=default_config['port'], type=int)
    parser.add_argument('-address', help='client address to bind', default=default_config['address'])
    parser.add_argument('-port', help='client port to bind', type=int)
    return vars(parser.parse_args())


def get_server_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-address', help='server address to bind', default=default_config['address'])
    parser.add_argument('-port', help='server port to bind', default=default_config['port'])
    return vars(parser.parse_args())