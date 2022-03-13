DROP TABLE IF EXISTS bruker;
DROP TABLE IF EXISTS sesjon;
DROP TABLE IF EXISTS dikt;

CREATE TABLE bruker(
        epostadresse TEXT NOT NULL,
        passordhash TEXT,
        fornavn TEXT,
        etternavn TEXT,
        PRIMARY KEY (epostadresse)
);

CREATE TABLE sesjon(
        sesjonsID NUMBER NOT NULL,
        epostadresse TEXT,
        PRIMARY KEY (sesjonsID),
        FOREIGN KEY (epostadresse) REFERENCES bruker (epostadresse)
);

CREATE TABLE dikt(
        diktID NUMBER NOT NULL,
        dikt TEXT,
        epostadresse TEXT,
        PRIMARY KEY (diktID),
        FOREIGN KEY (epostadresse) REFERENCES bruker (epostadresse)
);
