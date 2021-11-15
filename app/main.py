from fastapi import FastAPI
from database import Database
from applogger import get_logger

app = FastAPI()
logger = get_logger()
database = Database(logger)

from routes import *
