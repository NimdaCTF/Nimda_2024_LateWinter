import sys
import hmac
import os
import hashlib
import zipfile
from shutil import rmtree

PREFIX = "nimda_w3lcome_to_the_jungle_"
SECRET = b"liquid-salve-it-et-universitas-novi-eboracum-quinque"
SALT_SIZE = 12


def get_salt():
    user_id = sys.argv[1]
    return hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    target = sys.argv[2]
    input_file = 'raw.wav'
    output_file = os.path.join(target, 'result.wav')

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    user_tmp = os.path.join('tmp', hashlib.md5(user_id.encode()).hexdigest())

    if not os.path.exists(user_tmp):
        os.mkdir(user_tmp)

    with open(os.path.join(user_tmp, 'Second_part_of_flag.txt'), 'w', encoding='UTF-8') as f:
        f.write(get_salt())

    archive_path = os.path.join(user_tmp, 'flag.zip')
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(os.path.join(user_tmp, 'Second_part_of_flag.txt'), 'Second_part_of_flag.txt')

    with open(output_file, 'wb') as of:
        with open(input_file, 'rb') as _if:
            with open(archive_path, 'rb') as af:
                of.write(_if.read())
                of.write(chr(0).encode() * 100)
                of.write(af.read())

    rmtree(user_tmp)


if __name__ == '__main__':
    generate()
