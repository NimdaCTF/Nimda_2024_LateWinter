from checklib import *
import requests
from random import choice
from string import ascii_letters, digits
from uuid import uuid4
from bs4 import BeautifulSoup
from base64 import encodebytes


class CheckMachine:
    @property
    def url(self):
        return f"http://{self.c.host}/index.php"

    def generate_username(self):
        return str(uuid4())

    def generate_random_string(self, length=30) -> str:
        return "".join([choice(ascii_letters + digits) for _ in range(length)])

    @property
    def login_creds(self):
        return {"username": self.user, "password": self.password, "auth_type": "special"}

    @property
    def signup_creds(self):
        return {"username": self.user, "password": self.password, "signup_type": "special"}

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = 8500
        self.user = self.generate_username()[:20].replace("-", "")
        self.password = self.generate_random_string()

    def default_status_check(self, response, method, status, check_json=True):
        self.c.assert_eq(response.status_code, 200, f"Bad status code on {method}", status)

        if check_json:
            data = self.c.get_json(response, f"Invalid response on {method}", status)

            self.c.assert_eq(type(data), dict, f"Invalid response type on {method}", status)
            self.c.assert_in("status", data, f"No status field on {method}", status)
            self.c.assert_eq(data["status"], True, f"Not status true on {method}", status)

            return data

        return None

    def auth(self, session: requests.Session, status: Status) -> bool:
        response = session.post(f"{self.url}", json=self.signup_creds | {"method": "signup"})
        self.default_status_check(response, "signup", status)

        response = session.post(f"{self.url}", json=self.login_creds | {"method": "auth"})
        self.default_status_check(response, "auth", status)

        response = session.post(f"{self.url}", json={"method": "logout"})
        self.default_status_check(response, "logout", status)

        response = session.post(f"{self.url}", json=self.login_creds | {"method": "auth"})
        self.default_status_check(response, "auth", status)

        response = session.post(
            f"{self.url}",
            json={
                "snp": f"{self.generate_random_string(7)} {self.generate_random_string(7)}",
                "group_id": 1,  # IDK
                "method": "initUser",
            },
        )
        self.default_status_check(response, "initUser", status)

        return True

    def general_methods(self, session: requests.Session, status: Status):
        response = session.get(f"{self.url}?method=getUser")
        self.default_status_check(response, "getUser", status)

        response = session.get(f"{self.url}?method=getInstitutesList")
        data = self.default_status_check(response, "getInstitutesList", Status)
        self.c.assert_in("values", data, f"No values field on getInstitutesList", status)
        self.c.assert_eq(
            bool([x for x in data["values"] if x["id"] == 1]), True, f"Empty institutes at getInstitutesList", status
        )

        response = session.get(f"{self.url}?method=getGroupsByInstitute&institute_id=1")
        data = self.default_status_check(response, "getGroupsByInstitute", status)
        self.c.assert_in("values", data, f"No values field on getGroupsByInstitute", status)
        self.c.assert_eq(
            bool([x for x in data["values"] if x["id"] == 1]), True, f"Empty groups at getGroupsByInstitute", status
        )

        response = session.get(f"{self.url}?method=getStudentsByGroup&group_id=1")
        self.default_status_check(response, "getGroupsByInstitute", status)
        secret = "SupA_SecRet"
        response = session.post(f"{self.url}", json={"newSecret": secret, "method": "updateSecret"})
        self.default_status_check(response, "updateSecret", status)
        response = session.get(f"{self.url}?method=getUser")
        data = self.default_status_check(response, "getUser", status)

        self.c.assert_in("passport", data, f"No passport field on getUser", status)
        self.c.assert_eq(secret == data["passport"], True, f"Secrets do not equal", status)

    def secondary_methods(self, session: requests.Session, status: Status) -> bool:
        response = session.get(f"{self.url}?method=getGroupRating")
        self.default_status_check(response, "/getGroupRating", status)

        response = session.get(f"{self.url}?method=getGlobalRating")
        self.default_status_check(response, "/getGlobalRating", status)

        response = session.get(f"{self.url}?method=getGroupSubjects")
        self.default_status_check(response, "/getGroupSubjects", status)

        response = session.get(f"{self.url}?method=getStudentMarks")
        self.default_status_check(response, "/getStudentMarks", status)

        response = session.get(f"{self.url}?method=getCurrentSubjects&semester=1")
        self.default_status_check(response, "/getCurrentSubjects", status)

        response = session.get(f"{self.url}?method=getSubjectById&id=1")
        self.default_status_check(response, "/getSubjectById", status)

        response = session.get(f"{self.url}?method=getTasksBySubject&id=1")
        self.default_status_check(response, "/getTasksBySubject", status)

        response = session.get(f"{self.url}?method=getTaskById&id=1")
        self.default_status_check(response, "/getTaskById", status)

        return True

    def upload_file(self, session: requests.Session, status: Status):
        response = session.get(f"{self.url}?method=getCurrentSubjects&semester=1")
        data = self.default_status_check(response, "/getCurrentSubjects", status)
        self.c.assert_in("values", data, f"No values field on getCurrentSubjects", status)
        self.c.assert_eq(len(data["values"]) > 1, True, f"Empty subjects at getCurrentSubjects", status)

        data = data["values"][0]
        self.c.assert_in("id", data, f"Empty id at getCurrentSubjects", status)

        s_id = data["id"]

        response = session.get(f"{self.url}?method=getTasksBySubject&id={s_id}")
        data = self.default_status_check(response, "getTasksBySubject", status)

        self.c.assert_in("values", data, f"No values field on getTasksBySubject", status)
        self.c.assert_eq(len(data["values"]) > 1, True, f"Empty values at getTasksBySubject", status)

        data = data["values"][0]
        self.c.assert_in("id", data, f"Empty id at getTasksBySubject", status)

        t_id = data["id"]
        raw_payload = b"kekwait"
        payload = encodebytes(raw_payload).decode("UTF-8")
        response = session.get(
            f"{self.url}",
            json={"method": "uploadFile", "file": payload, "taskId": t_id, "filename": self.generate_random_string(10)},
        )
        self.default_status_check(response, "uploadFile", status)

        response = session.get(f"{self.url}?method=loadFile&id={t_id}")
        self.c.assert_eq(response.content == raw_payload, True, f"Invalid load_file", status)

    def add_flag(self, session: requests.Session, flag: str, status: Status):
        username = self.generate_username()[:20].replace("-", "")
        password = self.generate_random_string(30)

        response = session.post(
            f"{self.url}",
            json={"method": "signup", "username": username, "password": password, "signup_type": "special"},
        )
        self.default_status_check(response, "signup", status)

        response = session.post(
            f"{self.url}", json={"method": "auth", "username": username, "password": password, "auth_type": "special"}
        )
        self.default_status_check(response, "auth", status)

        response = session.post(f"{self.url}", json={"newSecret": flag, "method": "updateSecret"})
        self.default_status_check(response, "updateSecret", status)
        response = session.get(f"{self.url}?method=getUser")
        data = self.default_status_check(response, "getUser", status)

        self.c.assert_in("passport", data, f"No passport field on getUser", status)
        self.c.assert_eq(flag == data["passport"], True, f"Secrets do not equal", status)

        print(username, password)

        return username, password

    def check_flag(self, session: requests.Session, flag: str, credentials, status: Status):
        username = credentials["username"]
        password = credentials["password"]

        response = session.post(
            f"{self.url}", json={"method": "auth", "username": username, "password": password, "auth_type": "special"}
        )
        self.default_status_check(response, "auth", status)

        response = session.get(f"{self.url}?method=getUser")
        data = self.default_status_check(response, "getUser", status)

        self.c.assert_in("passport", data, f"No passport field on getUser", status)
        self.c.assert_eq(flag == data["passport"], True, f"Secrets do not equal", status)
