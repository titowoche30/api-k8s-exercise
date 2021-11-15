from typing import Optional


class ApiUser:
    def __init__(self, name: str, login: str, password: str, email: str, id: Optional[int] = None):
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.id = id

    def __str__(self):
        return f'Name: {self.name} login:{self.login} password:{self.password} email: {self.email} id: {self.id}'
