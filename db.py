import sqlite3
from flask import g

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            event_time DATETIME,
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
            signup_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(event_id, user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE event_types (
            id INTEGER PRIMARY KEY,
            title TEXT
        )
    ''')
    event_types = ['Sitsit', 'Bileet', 'Appro', 'Excu', 'Risteily', 'Liikunta', 'Tapaaminen', 'Muu']
    for event_type in event_types:
        cursor.execute('INSERT INTO event_types (title) VALUES (?)', (event_type,))
    conn.commit()
    conn.close()

def get_connection():
    con = sqlite3.connect("database.db")
    con.set_trace_callback(print)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
    return result

def last_insert_id():
    return g.last_insert_id    
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result