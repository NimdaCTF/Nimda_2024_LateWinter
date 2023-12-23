from random import choice, randint
import sys
import hmac
import os
import hashlib
from shutil import rmtree
from string import ascii_letters, digits
import zipfile

PREFIX = "nimda_s0m371me$_We_CaN_H1d3_the_F1les_Lik3_ThiS_"
SECRET = b"non-different-in-urbe-essen-ich-heibe-ikla-cloud9"
SALT_SIZE = 12


def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def get_random_str(length: int):
    return ''.join([choice(ascii_letters + digits) for _ in range(length)])


def add_folder_to_zip(zipf, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_path)
            zipf.write(file_path, arcname=arcname)


f_num = 0


def create_folders(base_dir, num_folders, depth, magic_number):
    global f_num

    if depth == 0:
        return
    for i in range(num_folders):
        folder_name = get_random_str(randint(6, 128))
        folder_path = os.path.join(base_dir, folder_name)
        os.makedirs(folder_path)
        f_num += 1
        with open(os.path.join(folder_path, 'flag.txt'), 'w', encoding='UTF-8') as f:
            if f_num == magic_number:
                f.write(get_flag())
            else:
                f.write('Not a flag XD')

        create_folders(folder_path, num_folders, depth - 1, magic_number)


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

    magic_number = randint(1000, 11100)
    create_folders(user_path, 10, 4, magic_number)

    with zipfile.ZipFile(os.path.join(target, 'result.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        add_folder_to_zip(zipf, user_path)

    rmtree(user_path)


if __name__ == '__main__':
    generate()
