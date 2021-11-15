from typing import List
from main import app, database, logger
from apiuserdao import ApiUserDAO
from apiuser import ApiUser, ApiUserModel
from database_errors import UniqueViolation


@app.on_event("startup")
async def startup_event():
    database.execute_database_startup()


@app.get('/')
async def root():
    return {"Message": "Hello meu xapa"}


@app.get('/user/{id}')
async def retrieve_user_by_id(id: int):
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    logger.info(f"[API] Retrieving user by id {id}")
    api_user = api_user_dao.retrieve(id)

    database.close_connection(conn)

    if not api_user:
        return {f'User {id} not found'}

    api_user_model = ApiUserModel(name=api_user[1],
                                  login=api_user[2],
                                  password=api_user[3],
                                  email=api_user[4],
                                  id=api_user[0])

    response = api_user_model.dict()

    return response


@app.get('/users/')
async def retrieve_users():
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    logger.info(f"[API] Retrieving users ")
    api_users = api_user_dao.retrieve_all()

    database.close_connection(conn)

    if not api_users:
        return {f'No users were found'}

    api_users_objects = [ApiUserModel(name=api_user[1],
                                      login=api_user[2],
                                      password=api_user[3],
                                      email=api_user[4],
                                      id=api_user[0]) for api_user in api_users]

    return api_users_objects


@app.get('/user-login/{login}')
async def retrieve_user_by_login(login: str):
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    logger.info(f"[API] Retrieving user by login {login}")
    api_user = api_user_dao.retrieve_by_login(login)

    database.close_connection(conn)

    if not api_user:
        return {f'User {login} not found'}

    api_user_model = ApiUserModel(name=api_user[1],
                                  login=api_user[2],
                                  password=api_user[3],
                                  email=api_user[4],
                                  id=api_user[0])

    response = api_user_model.dict()

    return response


@app.post('/user/')
async def create_or_update_user(user: ApiUserModel):
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    user_dict = user.dict()
    user_dict.pop('id')
    logger.info(f"[API] Upserting user {user_dict}")

    api_user = ApiUser(user.name, user.login, user.password, user.email, user.id)
    try:
        api_user_dao.upsert(api_user)
    except UniqueViolation as e:
        logger.info("[POSTGRES] Not able to insert user due to UniqueViolation")
        return {'error': 'Duplicate key value violates unique constraint'}

    inserted_user = api_user_dao.retrieve_by_login(api_user.login)
    inserted_user_id = inserted_user[0]
    inserted_user_login = inserted_user[2]

    database.close_connection(conn)

    response = user.dict()
    response['id'] = inserted_user_id
    response['login'] = inserted_user_login
    response['upsert'] = True

    return response


@app.delete('/user/{id}')
async def delete_user_by_id(id: int):
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    logger.info(f"[API] Deleting user by id {id}")
    api_user_dao.delete(id)

    database.close_connection(conn)

    response = {'id': id, 'delete': True}
    return response


@app.delete('/user-login/{login}')
async def delete_user_by_login(login: str):
    conn = database.get_connection('fastapi')
    api_user_dao = ApiUserDAO(conn)

    logger.info(f"[API] Deleting user by login {login}")
    api_user_dao.delete_by_login(login)

    database.close_connection(conn)

    response = {'login': login, 'delete': True}
    return response

