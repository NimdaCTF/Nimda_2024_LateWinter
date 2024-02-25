#!/usr/bin/env python3
import sys
import os

import json
from check_machine import *
from checklib import BaseChecker
from base64 import b64decode, b64encode

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def decodebytes(inp: bytes) -> bytes:
    return b64decode(inp)


def encodebytes(inp: bytes) -> bytes:
    return b64encode(inp)


class Checker(BaseChecker):
    vulns: int = 2
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

    def check(self):
        session = get_initialized_session()
        self.mch.auth(session, Status.CORRUPT)
        self.mch.general_methods(session, Status.CORRUPT)
        self.mch.secondary_methods(session, Status.MUMBLE)
        self.mch.upload_file(session, Status.MUMBLE)

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        username, password = self.mch.add_flag(session, flag, Status.CORRUPT)
        self.cquit(
            Status.OK,
            encodebytes(json.dumps({"username": username, "password": password}).encode()).decode("UTF-8"),
        )

    def get(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        creds = json.loads(decodebytes(flag_id.encode()).decode("UTF-8"))

        self.mch.check_flag(session, flag, creds, Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == "__main__":
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
