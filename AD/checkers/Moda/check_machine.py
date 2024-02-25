from checklib import *
import requests
from random import choice
from string import ascii_letters, digits
from uuid import uuid4


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}'

    def generate_username(self):
        return f'{str(uuid4())}@{self.generate_random_string(5)}.{self.generate_random_string(2)}'

    def generate_random_string(self, length=30) -> str:
        return ''.join([choice(ascii_letters + digits) for _ in range(length)])

    @property
    def creds(self):
        return {
            'username': self.user,
            'password': self.password
        }

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = 8501
        self.user = self.generate_username()
        self.password = self.generate_random_string()
        self.created_post_ids = {}

    def auth(self, session: requests.Session, status: Status) -> bool:
        response = session.post(f'{self.url}/auth/register', json={
            "email": self.user,
            "password": self.password,
            "username": self.user
        })

        self.c.assert_eq(response.status_code, 201, "Bad status code on /register", status)

        data = self.c.get_json(
            response, "Invalid response on /register", status)

        self.c.assert_eq(type(data), dict,
                         "Invalid response type on /register", status)
        self.c.assert_in("is_active", data, "No is_active field on /register", status)
        self.c.assert_eq(data["is_active"], True, "Not is_active true on /register", status)

        response = session.post(f'{self.url}/auth/jwt/login', data=self.creds)
        self.c.assert_eq(response.status_code, 204, "Bad status code on /login", status)

        session.cookies['moda_ctf_auth'] = session.cookies['moda_ctf_auth'].replace('b\'', '').replace('\'', '')

        return True

    def change_login(self, session: requests.Session, status: Status) -> bool:
        new_username = self.generate_random_string(5)
        response = session.put(f'{self.url}/user/update', json={"email": self.user, "username": new_username})

        self.c.assert_eq(response.status_code, 200, "Bad status code on /user/update", status)

        data = session.get(f'{self.url}/user')
        data = self.c.get_json(
            response, "Invalid response on /user", status)

        self.c.assert_eq(type(data), dict,
                         "Invalid response type on /user", status)
        self.c.assert_in("username", data, "No username field on /user", status)
        self.c.assert_eq(data["username"], new_username, "Can\'t set username on /user", status)

        return True

    def add_flag(self, sess: requests.Session, flag: str, status):
        username = self.generate_username()
        password = self.generate_random_string()

        response = sess.post(f'{self.url}/auth/register', json={
            'email': username,
            'username': username,
            'password': password
        })

        self.c.assert_eq(response.status_code, 201, "Bad status code on /register", status)

        response = sess.post(f'{self.url}/auth/jwt/login', data={'username': username, 'password': password})
        self.c.assert_eq(response.status_code, 204, "Bad status code on /login", status)

        sess.cookies['moda_ctf_auth'] = sess.cookies['moda_ctf_auth'].replace('b\'', '').replace('\'', '')

        data = sess.put(f'{self.url}/user/update', json={"email": self.user, "username": flag})

        self.c.assert_eq(data.status_code, 200, "Bad status code on /user/update", status)

        data = sess.get(f'{self.url}/user')
        data = self.c.get_json(
            data, "Invalid response on /user", status)

        self.c.assert_eq(type(data), dict,
                         "Invalid response type on /user", status)
        self.c.assert_in("username", data, "No username field on /user", status)
        self.c.assert_eq(data["username"], flag, "Can\'t set username on /user/update", status)

        return username, password

    def check_flag(self, sess: requests.Session, flag: str, creds: dict, status):
        response = sess.post(f'{self.url}/auth/jwt/login', data=creds)
        self.c.assert_eq(response.status_code, 200, "Bad status code on /login", status)

        response = sess.get(f'{self.url}/user')
        data = self.c.get_json(
            response, "Invalid response on /user", status)

        self.c.assert_eq(type(data), dict,
                         "Invalid response type on /user", status)
        self.c.assert_in("username", data, "No username field on /user", status)
        self.c.assert_eq(data["username"], flag, "Can\'t set username on /user/update", status)

        return True
