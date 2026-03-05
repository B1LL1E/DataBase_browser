from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictConnection

load_dotenv()

app = Flask(__name__)
serialeDB_env = os.getenv("serialeDB")

DATABASE_URL = os.getenv('DATABASE_URL', serialeDB_env)



print(DATABASE_URL)

#LOKALNIE CZY ONLINE?
if DATABASE_URL:
    print("POSTGRESQL")
    #laczy z baza PostgreSQL
    def get_db_conn():
        conn = psycopg2.connect(DATABASE_URL)
        #wszystko ma byc na zywo zapisywane
        conn.autocommit = True
        return conn
    DB_TYPE = 'postgres'

else:
    print("sqlite3")
    #tylko lokalnie
    import sqlite3
    DB_PATH = 'seriale.db'
    DB_TYPE = 'sqlite'





#glowne polaczenie
@app.route('/')
def index():
    if DB_TYPE == 'postgres':
        conn = get_db_conn()
        cur = conn.cursor(cursor_factory=RealDictConnection)
    else:
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    cur.execute('SELECT * FROM seriale ORDER BY id DESC')
    seriale = cur.fetchall()
    conn.close()
    return render_template('index.html', seriale = seriale)





@app.route('/add', methods = ['POST'])
def add_serial():
    tytul = request.form['tytul']
    nr_odc_poczatek = request.form['nr_odc_poczatek']
    nr_odc_koniec = request.form['nr_odc_koniec']
    opis = request.form['opis']
    avt = request.form['AVT']
    jezyk = request.form['jezyk']
    autor_avt = request.form['autor_avt']
    zrodlo = request.form['zrodlo']

    if DB_TYPE == 'postgres':
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO seriale (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo))
        conn.close()
    else:
        conn = sqlite3.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO seriale (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo))
        conn.commit()
        conn.close()
    return redirect('/')


if __name__ == '__main__':
    # TYLKO lokalnie SQLite
    if DB_TYPE == 'sqlite':
        conn = sqlite3.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS seriale(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tytul TEXT,
                nr_odc_poczatek INTEGER,
                nr_odc_koniec INTEGER,
                opis TEXT,
                avt TEXT NOT NULL,
                jezyk TEXT NOT NULL,
                autor_avt TEXT,
                zrodlo TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
    
    app.run(debug=True)

