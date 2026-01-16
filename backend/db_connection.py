"""
Module de connexion à la base de données MySQL
Adapté pour le cloud (PlanetScale, Aiven, etc.)
"""
import mysql.connector
from mysql.connector import Error
import os
import streamlit as st

class DatabaseConnection:
    """Classe pour gérer la connexion à la base de données"""
    
    def __init__(self):
        """Initialiser la connexion"""
        self.connection = None
        self.host = st.secrets.get("DB_HOST", "localhost")
        self.port = int(st.secrets.get("DB_PORT", "3306"))
        self.database = st.secrets.get("DB_NAME", "edt_examens")
        self.user = st.secrets.get("DB_USER", "root")
        self.password = st.secrets.get("DB_PASSWORD", "")
        
        # For PlanetScale/cloud databases
        self.use_ssl = st.secrets.get("DB_USE_SSL", "False").lower() == "true"
        self.ssl_ca = st.secrets.get("DB_SSL_CA", None)
    
    def connect(self):
        """Établir la connexion à la base de données"""
        try:
            if self.connection is None or not self.connection.is_connected():
                connection_config = {
                    "host": self.host,
                    "port": self.port,
                    "database": self.database,
                    "user": self.user,
                    "password": self.password,
                    "autocommit": True,
                    "buffered": True
                }
                
                # Add SSL for cloud databases
                if self.use_ssl:
                    connection_config["ssl_disabled"] = False
                    if self.ssl_ca:
                        connection_config["ssl_ca"] = self.ssl_ca
                    else:
                        connection_config["ssl_verify_cert"] = True
                        connection_config["ssl_verify_identity"] = True
                
                self.connection = mysql.connector.connect(**connection_config)
                
                if self.connection.is_connected():
                    print(f"✅ Connecté à MySQL: {self.database}")
                    return self.connection
            return self.connection
        except Error as e:
            print(f"❌ Erreur de connexion MySQL: {e}")
            # Fallback to SQLite for demo
            return self._fallback_to_sqlite()
    
    def _fallback_to_sqlite(self):
        """Fallback to SQLite if MySQL fails (for demo/debugging)"""
        print("⚠️ Tentative de connexion à SQLite...")
        try:
            import sqlite3
            # Create SQLite database if it doesn't exist
            conn = sqlite3.connect('exam_demo.sqlite')
            conn.row_factory = sqlite3.Row
            
            # Create basic tables
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    nom TEXT,
                    prenom TEXT,
                    email TEXT,
                    role TEXT
                )
            ''')
            
            # Add demo data
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, nom, prenom, email, role) 
                VALUES 
                ('admin', 'admin123', 'Admin', 'User', 'admin@univ.edu', 'admin'),
                ('prof1', 'prof123', 'John', 'Doe', 'prof@univ.edu', 'professeur'),
                ('etud1', 'etud123', 'Jane', 'Smith', 'etud@univ.edu', 'etudiant')
            ''')
            
            conn.commit()
            print("✅ Connecté à SQLite (fallback)")
            
            # Create a wrapper to make SQLite look like MySQL
            class SQLiteWrapper:
                def __init__(self, conn):
                    self.conn = conn
                    self.is_connected = lambda: True
                
                def cursor(self, dictionary=False, buffered=False):
                    return self.conn.cursor()
                
                def close(self):
                    self.conn.close()
                
                def commit(self):
                    self.conn.commit()
            
            self.connection = SQLiteWrapper(conn)
            return self.connection
            
        except Exception as e:
            print(f"❌ Échec de SQLite aussi: {e}")
            return None
    
    def disconnect(self):
        """Fermer la connexion"""
        if self.connection:
            try:
                self.connection.close()
                print("✅ Connexion fermée")
            except:
                pass
    
    def execute_query(self, query, params=None):
        """
        Exécuter une requête SELECT
        """
        cursor = None
        try:
            conn = self.connect()
            if conn:
                # Handle fallback SQLite connection
                if hasattr(conn, '__class__') and 'SQLiteWrapper' in str(conn.__class__):
                    cursor = conn.cursor()
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    if query.strip().upper().startswith('SELECT'):
                        rows = cursor.fetchall()
                        # Convert to list of dicts for compatibility
                        columns = [desc[0] for desc in cursor.description] if cursor.description else []
                        return [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
                    else:
                        conn.commit()
                        return True
                else:
                    # Original MySQL code
                    cursor = conn.cursor(dictionary=True, buffered=True)
                    
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    if query.strip().upper().startswith('SELECT'):
                        return cursor.fetchall()
                    else:
                        conn.commit()
                        return True
            return None
        except Error as e:
            print(f"❌ Erreur MySQL: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

# Instance globale
db = DatabaseConnection()

# Fonctions utilitaires
def get_connection():
    return db.connect()

def execute_query(query, params=None):
    return db.execute_query(query, params)
