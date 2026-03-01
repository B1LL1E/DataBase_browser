from flask import Flask, render_template, request, redirect
import sqlite3
#from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#DB_PATH = 'seriale.db'
#
if os.getenv('DATABASE_URL'):
    import psycopg2
    from psycopg2.extras import RealDictConnection
    DB_PATH = os.getenv('DATABASE_URL')
    DB_TYPE = 'postgres'
else:
    DB_PATH = 'seriale.db'
    DB_TYPE = 'sqlite'

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM seriale')
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

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO seriale (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,)', (tytul, nr_odc_poczatek, nr_odc_koniec, opis, avt, jezyk, autor_avt, zrodlo))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS seriale(
                    id SERIAL PRIMARY KEY,
                    tytul TEXT,
                    nr_odc_poczatek INTEGER,
                    nr_odc_koniec INTEGER,
                    opis TEXT,
                    avt TEXT NOT NULL CHECK(avt IN ('dubbing', 'lektor', 'napisy', 'inne')),
                    jezyk TEXT NOT NULL CHECK(jezyk IN ('polski', 'english', 'inne')),
                    autor_avt TEXT,
                    zrodlo TEXT NOT NULL
                );
                ''')
    conn.commit()
    conn.close()
    app.run(debug=True)


