import hmac
from core import flag_config


def generate_flag(user_id):
    PREFIX = flag_config['prefix']
    SECRET = flag_config['secret'].encode()
    SALT_SIZE = flag_config['salt_size']

    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]
