from _socket import SHUT_RD
from checklib import *
import requests
from random import choice
from string import ascii_letters, digits
from uuid import uuid4
from bs4 import BeautifulSoup
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from time import sleep
import json
from ftplib import FTP

MESSAGES_QUEUE = []
'''
Поздравляю всех с тем, что у разраба pycraft сдохли 2 отца

НЕ РАБОТАЕТ

from pyCraft.minecraft.networking.connection import Connection

connection.options.address = self.c.host
connection.options.port = 25565
connection.username = self.user

def handle_join_game(join_game_packet):
    print('Connected.')

connection.register_packet_listener(
    handle_join_game, clientbound.play.JoinGamePacket)

def print_chat(chat_packet):
    print("Message (%s): %s" % (
        chat_packet.field_string('position'), chat_packet.json_data))

connection.register_packet_listener(
    print_chat, clientbound.play.ChatMessagePacket)
    
РАБОТАЕТ

from minecraft.networking.connection import Connection

connection.options.address = self.c.host
connection.options.port = 25565
connection.username = self.user

def handle_join_game(join_game_packet):
    print('Connected.')

connection.register_packet_listener(
    handle_join_game, clientbound.play.JoinGamePacket)

def print_chat(chat_packet):
    print("Message (%s): %s" % (
        chat_packet.field_string('position'), chat_packet.json_data))

connection.register_packet_listener(
    print_chat, clientbound.play.ChatMessagePacket)
'''


class CheckMachine:
    @property
    def url(self):
        return f'{self.c.host}:{self.port}'

    def generate_random_string(self, length=30) -> str:
        return ''.join([choice(ascii_letters + digits) for _ in range(length)])

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = 25565
        self.user = self.generate_random_string(5)
        self.password = self.generate_random_string(10)

    def __login(self, connection, status):
        global MESSAGES_QUEUE

        packet = serverbound.play.ChatPacket()

        self.created_post = self.generate_random_string(5)
        packet.message = f'/login {self.password}'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if 'You logged in' not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.DOWN)
            sleep(1)

        MESSAGES_QUEUE.clear()

    def __register(self, connection, status):
        global MESSAGES_QUEUE

        packet = serverbound.play.ChatPacket()

        packet.message = f'/register {self.password} {self.password}'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if 'You have registered' not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.DOWN)
            sleep(1)

        MESSAGES_QUEUE.clear()

    def connect(self, connection: Connection, status: Status) -> bool:
        global MESSAGES_QUEUE

        connection.options.address = self.c.host
        connection.options.port = 25565
        connection.username = self.user

        def handle_join_game(join_game_packet):
            pass
            # print('Connected.')

        connection.register_packet_listener(
            handle_join_game, clientbound.play.JoinGamePacket)

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        retries = 0
        connection.connect()

        while True:
            if connection.connected:
                break
            retries += 1
            self.c.assert_neq(retries, 3, "Connection refused", status.DOWN)
            sleep(1)

        self.__register(connection, status)
        self.__login(connection, status)

        return True

    def add_note(self, connection: Connection, status: Status) -> bool:
        global MESSAGES_QUEUE

        connection.packet_listeners.clear()

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        self.c.assert_eq(connection.connected, True, "Connection refused", status.DOWN)
        packet = serverbound.play.ChatPacket()

        self.created_post = self.generate_random_string(5)
        packet.message = f'/nimda note add {self.created_post} 0'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if 'Successfully added' not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.DOWN)
            sleep(1)

        MESSAGES_QUEUE.clear()

        return True

    def get_note(self, connection: Connection, status: Status) -> bool:
        global MESSAGES_QUEUE

        connection.packet_listeners.clear()

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        self.c.assert_eq(connection.connected, True, "Connection refused", status.DOWN)
        packet = serverbound.play.ChatPacket()

        packet.message = f'/nimda note get {self.created_post}'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if self.created_post not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.CORRUPT)
            sleep(1)

        MESSAGES_QUEUE.clear()

        return True

    def check_ftp(self, ftp_connection: FTP, status: Status) -> bool:
        try:
            ftp_connection.connect(self.c.host)
        except:
            self.c.cquit(status.DOWN, 'Can\'t connect to FTP')

        try:
            ftp_connection.login('www-data', 'alpine')
        except:
            self.c.cquit(status.CORRUPT, 'Can\'t sign in FTP')

        return True

    def add_flag(self, connection: Connection, flag: str, status: Status):
        global MESSAGES_QUEUE

        connection.options.address = self.c.host
        connection.options.port = 25565
        connection.username = self.user

        def handle_join_game(join_game_packet):
            pass
            # print('Connected.')

        connection.register_packet_listener(
            handle_join_game, clientbound.play.JoinGamePacket)

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        retries = 0
        connection.connect()

        while True:
            if connection.connected:
                break
            retries += 1
            self.c.assert_neq(retries, 3, "Connection refused", status.DOWN)
            sleep(1)

        self.__register(connection, status)
        self.__login(connection, status)

        packet = serverbound.play.ChatPacket()

        packet.message = f'/nimda note add {flag} 1'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if 'Successfully added' not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.CORRUPT)
            sleep(1)

        MESSAGES_QUEUE.clear()

        return self.user, self.password

    def check_flag(self, connection: Connection, flag: str, username, password, status: Status):
        global MESSAGES_QUEUE

        connection.options.address = self.c.host
        connection.options.port = 25565
        connection.username = username

        self.user = username
        self.password = password

        def handle_join_game(join_game_packet):
            pass
            # print('Connected.')

        connection.register_packet_listener(
            handle_join_game, clientbound.play.JoinGamePacket)

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        retries = 0
        connection.connect()

        def print_chat(chat_packet):
            global MESSAGES_QUEUE
            MESSAGES_QUEUE.append(chat_packet.json_data)

        connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        self.c.assert_eq(connection.connected, True, "Connection refused", status.DOWN)

        self.__login(connection, status)

        packet = serverbound.play.ChatPacket()

        # А хули нам
        packet.message = f'/nimda note get {flag}'

        try:
            sleep(1)
            connection.write_packet(packet)
        except:
            self.c.cquit(status.DOWN, 'Connection refused')

        retries = 0

        def has_success_in_msg() -> bool:
            if len(MESSAGES_QUEUE) > 0:
                for i in MESSAGES_QUEUE:
                    try:
                        i = json.loads(i)
                    except:
                        continue
                    if not i.get('extra'):
                        continue
                    if not isinstance(i['extra'], list):
                        continue
                    if not i['extra'][0].get('text'):
                        continue
                    if flag not in i['extra'][0]['text']:
                        continue
                    else:
                        return True

            return False

        while not has_success_in_msg():
            retries += 1
            self.c.assert_neq(retries, 5, "Timed out waiting for response or response corrupted", status.CORRUPT)
            sleep(1)

        MESSAGES_QUEUE.clear()

        return True

    def check_ftp(self, ftp_connection: FTP, status: Status) -> bool:
        try:
            ftp_connection.connect(self.c.host)
        except:
            self.c.cquit(status.DOWN, 'Can\'t connect to FTP')

        try:
            ftp_connection.login('www-data', 'alpine')
        except:
            self.c.cquit(status.CORRUPT, 'Can\'t sign in FTP')

        return True
