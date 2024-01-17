from random import choice
import sys
import hmac
import os
import hashlib
from shutil import rmtree
from string import ascii_letters, digits
import pyzipper

PREFIX = "nimda_z1pP3d_dat@_wA$_F0unD_"
SECRET = b"ax1le-sh1ro-lecr0-s0mpl3-juggernaut-proxy-reversed"
SALT_SIZE = 12


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def get_random_str(length: int):
    return ''.join([choice(ascii_letters) for _ in range(length)])


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    target = sys.argv[2]

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    user_path = os.path.join('tmp', hashlib.md5(user_id.encode()).hexdigest())

    if not os.path.exists(user_path):
        os.mkdir(user_path)

    password = f'hard_as_hell_{get_random_str(4)}'

    # flag_file = os.path.join(user_path, 'flag.txt')
    # with open(flag_file, 'w', encoding='UTF-8') as f:
    #     f.write(get_flag())

    with pyzipper.AESZipFile(os.path.join(target, 'result.zip'),
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode())
        zf.writestr('flag.txt', get_flag())

    rmtree(user_path)


if __name__ == '__main__':
    generate()
