from multiprocessing import Process, freeze_support
from solver import connect, run


def subroutine():
    connect()
    while True:
        if not run():
            connect()
        else:
            break


if __name__ == '__main__':
    freeze_support()  # Add this line to support freezing on Windows

    procs = []

    for i in range(100):
        proc = Process(target=subroutine, name=f'P_{i}')
        procs.append(proc)

        proc.start()

        print(f'Process {proc.name} started')
