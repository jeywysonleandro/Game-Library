CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    senha TEXT NOT NULL,

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- TABELA DE JOGOS
CREATE TABLE IF NOT EXISTS jogos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    titulo TEXT NOT NULL,

    descricao TEXT,

    capa TEXT,

    nota REAL,

    status TEXT DEFAULT 'Quero jogar',

    favorito INTEGER DEFAULT 0,

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)

);