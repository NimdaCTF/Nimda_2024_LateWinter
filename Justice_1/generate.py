import os
from uuid import uuid4
from distutils.dir_util import copy_tree
import sys
import subprocess
from shutil import rmtree
import zipfile


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    target = os.path.abspath(sys.argv[2])

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    uid = str(uuid4())

    project_path = os.path.join('tmp', uid)
    if not os.path.exists(project_path):
        os.mkdir(project_path)

    project_result_path = os.path.abspath(os.path.join(project_path, 'result'))

    if not os.path.exists(project_result_path):
        os.mkdir(project_result_path)

    data_dep_path = os.path.join(project_path, 'DataDep')

    copy_tree('DataDep', data_dep_path)

    data = open(os.path.join(data_dep_path, 'Data.cs'), 'r', encoding='UTF-8').read()
    data = data.replace('XXX', user_id)
    open(os.path.join(data_dep_path, 'Data.cs'), 'w', encoding='UTF-8').write(data)
    os.chdir(data_dep_path)

    container_name = f'justice1_{uid}'

    try:
        result = subprocess.run(f'docker run --name {container_name} --detach --rm justice-dockyard')
        if result.returncode != 0:
            raise Exception()
        subprocess.run(f'docker cp {container_name}:/src/bin/Release/net6.0/. {project_result_path}')
    except:
        subprocess.run('docker build --no-cache -t justice-dockyard .')
        subprocess.run(f'docker run --name {container_name} --detach --rm justice-dockyard')
        subprocess.run(f'docker cp {container_name}:/src/bin/Release/net6.0/. {project_result_path}')
    finally:
        subprocess.run(f'docker kill {container_name}')
        os.chdir(os.path.realpath(__file__).replace('generate.py', ''))

    copy_tree('Pre-generated', project_result_path)
    with zipfile.ZipFile(os.path.join(target, 'result.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(project_result_path):
            file_path = os.path.join(project_result_path, file)
            zipf.write(file_path, os.path.basename(file_path))

    rmtree(project_path)


if __name__ == '__main__':
    generate()
