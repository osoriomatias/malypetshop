# -*- coding: utf-8 -*-
import os
import shutil
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "database", "petshop.db")
TMP_DB = "/tmp/pellegrini_petshop.db"

def get_connection():
    if not os.path.exists(TMP_DB) and os.path.exists(DB_FILE):
        try:
            shutil.copyfile(DB_FILE, TMP_DB)
        except Exception:
            pass

    use_tmp = False
    try:
        test = sqlite3.connect(DB_FILE, timeout=1)
        test.execute("PRAGMA journal_mode = MEMORY")
        test.execute("CREATE TABLE IF NOT EXISTS _test_lock (x INT)")
        test.commit()
        test.close()
    except Exception:
        use_tmp = True

    target = TMP_DB if use_tmp else DB_FILE
    conn = sqlite3.connect(target, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def sync_to_disk():
    if os.path.exists(TMP_DB) and os.path.exists(DB_FILE):
        try:
            shutil.copyfile(TMP_DB, DB_FILE)
        except Exception:
            pass

def query_all(sql, params=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
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
        sync_to_disk()
        return last_id
    finally:
        conn.close()

def execute_many(sql, seq):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, seq)
        conn.commit()
        sync_to_disk()
        return True
    finally:
        conn.close()
