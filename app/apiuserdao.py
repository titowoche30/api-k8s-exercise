from apiuser import ApiUser

SQL_CREATE_USER = 'INSERT INTO apiuser (name, login, password, email) VALUES (%s, %s, %s, %s);'
SQL_RETRIEVE_USER = 'SELECT id, name, login, password, email FROM apiuser WHERE id = %s;'
SQL_RETRIEVE_USER_BY_LOGIN = 'SELECT id, name, login, password, email FROM apiuser WHERE login = %s;'
SQL_UPDATE_USER = 'UPDATE apiuser SET name=%s, login=%s, password=%s, email=%s WHERE id = %s;'
SQL_DELETE_USER = 'DELETE FROM apiuser WHERE id = %s;'
SQL_DELETE_USER_BY_LOGIN = 'DELETE FROM apiuser WHERE login = %s;'
SQL_RETRIEVE_USERS = 'SELECT id, name, login, password, email FROM apiuser;'
SQL_RETRIEVE_LOGINS = 'SELECT login FROM apiuser;'


class ApiUserDAO:
    def __init__(self, conn):
        self.conn = conn

    def upsert(self, user: ApiUser):
        cursor = self.conn.cursor()

        if user.id:
            cursor.execute(SQL_UPDATE_USER, (user.name, user.login, user.password, user.email, user.id))
        else:
            cursor.execute(SQL_CREATE_USER, (user.name, user.login, user.password, user.email))
            user.id = cursor.lastrowid

    def retrieve_all(self):
        cursor = self.conn.cursor()

        cursor.execute(SQL_RETRIEVE_USERS)

        return cursor.fetchall()

    def retrieve(self, id: int):
        cursor = self.conn.cursor()
        cursor.execute(SQL_RETRIEVE_USER, (id,))
        data = cursor.fetchone()
        return data

    def retrieve_by_login(self, login: str):
        cursor = self.conn.cursor()
        cursor.execute(SQL_RETRIEVE_USER_BY_LOGIN, (login,))
        data = cursor.fetchone()
        return data

    def delete(self, id: int):
        self.conn.cursor().execute(SQL_DELETE_USER, (id,))

    def delete_by_login(self, login: str):
        self.conn.cursor().execute(SQL_DELETE_USER_BY_LOGIN, (login,))
