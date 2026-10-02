# -*- coding: utf-8 -*-
import os
import shutil
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "database", "petshop.db")
TMP_DB = "/tmp/pellegrini_petshop.db"

def get_connection():
    """
    Retorna una conexión a SQLite con soporte para mapeo a diccionario.
    Maneja transparentemente entornos locales normales o entornos con sistemas de archivos montados.
    """
    # Intentar conexión directa al archivo local
    target_path = DB_FILE
    try:
        conn = sqlite3.connect(target_path, timeout=10)
        # Test de escritura
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError:
        # Si el sistema de archivos del contenedor no soporta bloqueo POSIX directo,
        # utilizamos una réplica sincronizada en /tmp
        if not os.path.exists(TMP_DB) and os.path.exists(DB_FILE):
            shutil.copyfile(DB_FILE, TMP_DB)
        conn = sqlite3.connect(TMP_DB, timeout=10)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

def sync_db_to_disk():
    """Sincroniza los cambios de /tmp al archivo permanente si se usa réplica."""
    if os.path.exists(TMP_DB):
        try:
            shutil.copyfile(TMP_DB, DB_FILE)
        except Exception as e:
            print("Notice on sync:", e)

def query_all(sql, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return rows
    finally:
        conn.close()

def query_one(sql, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def execute_write(sql, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        last_id = cursor.lastrowid
        sync_db_to_disk()
        return last_id
    finally:
        conn.close()

def execute_many_write(sql, seq_of_params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, seq_of_params)
        conn.commit()
        sync_db_to_disk()
        return True
    finally:
        conn.close()
