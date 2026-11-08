
-- =========================================
-- TABELA DE USUÁRIOS
-- =========================================

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    senha TEXT NOT NULL,

    perfil_publico INTEGER NOT NULL DEFAULT 0,

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- =========================================
-- TABELA DE JOGOS
-- =========================================

CREATE TABLE IF NOT EXISTS jogos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    -- IDENTIFICAÇÃO DO JOGO

    titulo TEXT NOT NULL,

    descricao TEXT,

    capa TEXT,

    identificador_api TEXT,

    data_lancamento TEXT,

    -- INFORMAÇÕES PERSONALIZADAS

    plataforma TEXT,

    genero TEXT,

    nota REAL,

    status TEXT NOT NULL DEFAULT 'Quero jogar',

    favorito INTEGER NOT NULL DEFAULT 0,

    data_inicio DATE,

    data_conclusao DATE,

    observacoes TEXT,

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)

);
