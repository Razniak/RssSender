-- tabela z zadaniami
DROP TABLE IF EXISTS rssemail;
CREATE TABLE rssemail (
    id integer primary key autoincrement, -- unikalny indentyfikator
    rss text not null, -- opis zadania do wykonania
    email text not null -- opis zadania do wykonania

);

-- pierwsze dane
INSERT INTO rssemail (id, rss, email)
VALUES (null, 'rss', "email");
