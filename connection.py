import sqlite3

def get_connection():
    # Veritabanı bağlantısı döndürür
    return sqlite3.connect("db.db")