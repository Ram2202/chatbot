# tests/test_connection.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.databases")
print("✅ Connected! Databases:", [row[0] for row in cursor.fetchall()])
conn.close()
