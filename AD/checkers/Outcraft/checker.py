#!/usr/bin/env python3
import sys
import os

import json
from check_machine import *
from base64 import b64decode, b64encode
from minecraft.networking.connection import Connection
from ftplib import FTP

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def decodebytes(inp: bytes) -> bytes:
    return b64decode(inp)


def encodebytes(inp: bytes) -> bytes:
    return b64encode(inp)


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 30
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, "Connection error", "Got requests connection error")

    def get_connection(self) -> Connection:
        return Connection(None, None)

    def check(self):
        connection = self.get_connection()
        connection_result = self.mch.connect(connection, Status.CORRUPT)
        add_note_result = self.mch.add_note(connection, Status.MUMBLE)
        get_note_result = self.mch.get_note(connection, Status.MUMBLE)
        ftp_connection = FTP()
        ftp_check = self.mch.check_ftp(ftp_connection, Status.CORRUPT)

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        connection = self.get_connection()
        if vuln == "1":
            private_username, private_password = self.mch.add_flag(connection, flag, Status.CORRUPT)
            self.cquit(
                Status.OK,
                encodebytes(json.dumps({"username": private_username, "password": private_password}).encode()).decode(
                    "UTF-8"
                ),
            )

    def get(self, flag_id: str, flag: str, vuln: str):
        connection = self.get_connection()
        creds = json.loads(decodebytes(flag_id.encode()).decode("UTF-8"))

        self.mch.check_flag(connection, flag, creds['username'], creds['password'], Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == "__main__":
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
