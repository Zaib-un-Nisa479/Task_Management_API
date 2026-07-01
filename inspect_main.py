import sqlite3
from main import app
from database import engine
import models

print('engine', engine)
print('before', sqlite3.connect('taskmanager.db').execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
models.Base.metadata.create_all(bind=engine)
print('after', sqlite3.connect('taskmanager.db').execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
