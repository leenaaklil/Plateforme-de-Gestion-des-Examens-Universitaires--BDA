"""
Module de connexion à la base de données MySQL (Streamlit Cloud compatible)
"""
import streamlit as st
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.host = st.secrets["DB_HOST"]
        self.port = int(st.secrets["DB_PORT"])
        self.database = st.secrets["DB_NAME"]
        self.user = st.secrets["DB_USER"]
        self.password = st.secrets["DB_PASSWORD"]

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    autocommit=True,
                    consume_results=True,
                    ssl_disabled=False  # REQUIRED
                )
            return self.connection
        except Error as e:
            st.error(f"❌ Erreur de connexion MySQL: {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        cursor = None
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor(dictionary=True, buffered=True)
                cursor.execute(query, params or ())
                if query.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
                    return cursor.fetchall()
                conn.commit()
                return True
        except Error as e:
            st.error(f"❌ Erreur SQL: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

db = DatabaseConnection()

def get_connection():
    return db.connect()

def execute_query(query, params=None):
    return db.execute_query(query, params)
