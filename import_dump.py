import sqlite3

# Nowa baza z tabelą seriale
conn = sqlite3.connect('seriale.db')
cursor = conn.cursor()

# Wczytaj i wykonaj dump.sql
with open('dump.sql', 'r') as f:
    sql = f.read()

cursor.executescript(sql)
conn.commit()
conn.close()

print("✅ Zaimportowano dump.sql do seriale.db!")
print("Tabela 'seriale_ac' zmieniona na 'seriale'")
