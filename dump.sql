BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "Seriale" (
    "id"              INTEGER PRIMARY KEY AUTOINCREMENT,
    "tytul"           TEXT NOT NULL,
    "nr_odc_poczatek" INTEGER NOT NULL,
    "nr_odc_koniec"   INTEGER NOT NULL,
    "opis"            TEXT,
    "AVT"             TEXT NOT NULL CHECK("AVT" IN ('dubbing', 'lektor', 'napisy', 'inne')),
    "jezyk"           TEXT NOT NULL CHECK("jezyk" IN ('polski', 'english', 'inne')),
    "Autor_AVT"       TEXT,
    "zrodlo"          TEXT NOT NULL
);

INSERT INTO "Seriale" (
    "tytul", 
    "nr_odc_poczatek", 
    "nr_odc_koniec", 
    "opis", 
    "AVT", 
    "jezyk", 
    "Autor_AVT", 
    "zrodlo"
) VALUES (
    'Naruto', 
    1, 
    104, 
    NULL, 
    'dubbing', 
    'polski', 
    'jetix', 
    'https://drive.google.com/drive/folders/1M5wgsQhr-tf0BnqmTkdY5ZSnLhN2vyhd'
);

COMMIT;