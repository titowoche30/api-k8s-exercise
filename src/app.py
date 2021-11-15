from fastapi import FastAPI
from Database import Database
# from pydantic import BaseModel
from AppLogger import get_logger
from ApiUserDAO import ApiUserDAO
from ApiUser import ApiUser

app = FastAPI()
logger = get_logger()
database = Database(logger)


@app.on_event("startup")
async def startup_event():
    database.execute_migrates()


@app.get('/')
async def root():
    return {"Message": "Hello meu xapa"}


@app.get('/{name}')
async def root(name: str):
    conn = database.get_connection('fastapi')
    apiuserdao = ApiUserDAO(conn)
    logger.info(f"[API] Inserting user {name}")

    example_user = ApiUser(name, 'login-teste', 'pass-teste', 'email-teste')
    apiuserdao.upsert(example_user)

    return {"Message": f"Hello {name}, you we're inserted"}

