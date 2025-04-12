import sqlite3
from flask import g

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            event_type TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signups (
            id INTEGER PRIMARY KEY,
            event_id INTEGER REFERENCES events(id),
            user_id INTEGER REFERENCES users(id),
            UNIQUE(event_id, user_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id    
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result