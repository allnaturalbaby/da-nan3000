CREATE TABLE bruker(
        epostadresse TEXT NOT NULL,
        passordhash TEXT,
        fornavn TEXT,
        etternavn TEXT,
        PRIMARY KEY (epostadresse)
);

CREATE TABLE sesjon(
        sesjonsID TEXT NOT NULL,
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
