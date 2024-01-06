import socket
import re
from random import randint
import traceback
from time import sleep
from datetime import datetime

R_INTERRUPT = 0.1

client_socket = socket.socket()

vocab = {}
retries = 0
reg = re.compile('''ReQuest says: (.*)
1. (\d+)
2. (\d+)
3. (\d+)
4. (\d+)''', re.MULTILINE)


def rand_besides(_from, to, besides: list):
    if len(besides) == (to - _from) + 1:
        raise RecursionError('Looped random')
    result = randint(_from, to)
    while result in besides:
        result = randint(_from, to)

    return result


def connect():
    global client_socket
    server_address = ('localhost', 8501)
    client_socket = socket.socket()
    client_socket.connect(server_address)


def construct_by_ix(results, tried):
    rx = []
    for x in results[1:]:
        if x in tried:
            rx.append(results.index(x))

    return rx


def get_previous_benchmark(_from):
    global vocab
    if len(vocab) in (0, 1):
        return 0

    for i, x in enumerate(sorted(vocab, reverse=False)):
        if x == _from:
            return vocab[list(vocab)[i - 1]]['benchmark']

    return 0


def run():
    global vocab, reg, client_socket, retries
    data = None

    try:
        client_socket.send(b'\n123')
        sleep(R_INTERRUPT)
        while True:
            if data is None:
                data = client_socket.recv(1024)
            if data == b'':
                client_socket.send(b'\n')
                sleep(R_INTERRUPT)
                # print('Data was null, continue')
                continue

            if 'nimda' in data.decode('UTF-8'):
                print(data.decode('UTF-8'))
                return True

            results = reg.findall(data.decode('UTF-8'))

            if isinstance(results, list):
                if len(results) >= 1:
                    results = results[0]
                    retries = 0
                else:
                    client_socket.send(b'\n')
                    sleep(R_INTERRUPT)
                    if retries > 3:
                        print(data.decode('UTF-8'))
                        return True
                    retries += 1
                    data = None
                    continue

            if results[0] not in vocab:
                vocab[results[0]] = {'tried': [], 'start_date': datetime.utcnow()}
                ind = rand_besides(1, 4, [])
                client_socket.send(f'{ind}\n'.encode())
                sleep(R_INTERRUPT)
                data = client_socket.recv(1024)
                if 'Good one' in data.decode('UTF-8'):
                    vocab[results[0]]['answer'] = results[ind]
                    vocab[results[0]]['benchmark'] = (datetime.utcnow() - vocab[results[0]]["start_date"]).microseconds
                    prev_bench = get_previous_benchmark(results[0])
                    print(
                        f'Ez got first blood {results[0]} => {results[ind]} for {vocab[results[0]]["benchmark"]}ms ({"+" if prev_bench < vocab[results[0]]["benchmark"] else "-"}{abs(prev_bench - vocab[results[0]]["benchmark"])}ms) ')
                else:
                    vocab[results[0]]['tried'].append(results[ind])
                    # print(f'Bad way for {results[0]} => {results[ind]}')
                    data = None
            else:
                if vocab[results[0]].get('answer') is not None:
                    ans_ind = results.index(vocab[results[0]]['answer'])
                    client_socket.send(f'{ans_ind}\n'.encode())
                    sleep(R_INTERRUPT)
                    data = client_socket.recv(1024)
                    if 'Good one' in data.decode('UTF-8'):
                        # vocab[results[0]]['answer'] = results[ans_ind]
                        # print(f'Pre-trained answer {results[0]} => {results[ans_ind]}')
                        continue
                    else:
                        vocab[results[0]]['tried'].append(results[ans_ind])
                        print(f'TF with {results[0]} => {results[ans_ind]}? Was pre-trained.')
                        data = None
                        exit(-1)

                ind = rand_besides(1, 4, construct_by_ix(results, vocab[results[0]]['tried']))
                client_socket.send(f'{ind}\n'.encode())
                sleep(R_INTERRUPT)
                data = client_socket.recv(1024)
                if 'Good one' in data.decode('UTF-8'):
                    vocab[results[0]]['answer'] = results[ind]
                    vocab[results[0]]['benchmark'] = (datetime.utcnow() - vocab[results[0]]["start_date"]).microseconds
                    prev_bench = get_previous_benchmark(results[0])

                    print(
                        f'Got {results[0]} => {results[ind]} for {vocab[results[0]]["benchmark"]}ms ({"+" if prev_bench < vocab[results[0]]["benchmark"] else "-"}{abs(prev_bench - vocab[results[0]]["benchmark"])}ms)')
                else:
                    vocab[results[0]]['tried'].append(results[ind])
                    # print(f'Bad way for {results[0]} => {results[ind]}')
                    data = None

            # print(results)
            # input()
    except ConnectionResetError:
        data = None
    except BrokenPipeError:
        data = None
    except RecursionError as e:
        print('Recursion')
        raise e
    except Exception as e:
        data = None
        print(e)
        traceback.print_exc()
    finally:
        client_socket.close()
        return False


if __name__ == '__main__':
    connect()
    while True:
        if not run():
            connect()
        else:
            break

    bench_sum = sum([vocab[x]['benchmark'] for x in vocab])
    print(f'In total: {bench_sum * 10 ** 6}s')
