from database import engine, DATABASE_URL
import models
import sqlite3

print('DATABASE_URL=', DATABASE_URL)
models.Base.metadata.create_all(bind=engine)
conn = sqlite3.connect('taskmanager.db')
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
conn.close()
