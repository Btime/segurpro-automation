import sqlite3

def create_table():
    conn = sqlite3.connect('segurpro.db')

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dados_json
                    (id INTEGER PRIMARY KEY, ROV_JSON INTEGER, STATUS_JSON TEXT, NOME_SITE_JSON TEXT, SISTEMA TEXT)''')

    conn.close()

def table_exist():
    conn = sqlite3.connect('segurpro.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados_json'")
    tabela = cursor.fetchone()

    conn.close()

def insert_data_json(rov, status, nome_site, sistema):
    conn = sqlite3.connect('segurpro.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dados_json (ROV_JSON, STATUS_JSON, NOME_SITE_JSON, SISTEMA) VALUES (?, ?, ?, ?)", (rov, status, nome_site, sistema))
    conn.commit()
    conn.close()