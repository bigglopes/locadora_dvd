import os
import sqlite3

class DatabaseConfig:
    """Classe para configuração e gerenciamento do banco de dados SQLite."""
    
    DB_FILE = "locadora.db"
    
    @classmethod
    def get_connection(cls):
        """Obtém uma conexão com o banco de dados.
        
        Returns:
            sqlite3.Connection: Conexão com o banco de dados.
        """
        # Verifica se o diretório database existe
        os.makedirs("database", exist_ok=True)
        
        # Cria a conexão com o banco de dados
        conn = sqlite3.connect(os.path.join("database", cls.DB_FILE))
        conn.row_factory = sqlite3.Row  # Para acessar as colunas pelo nome
        
        return conn
    
    @classmethod
    def initialize_database(cls):
        """Inicializa o banco de dados criando as tabelas necessárias."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT
        )
        """)
        
        # Adiciona coluna CPF se não existir (para compatibilidade com banco existente)
        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN cpf TEXT UNIQUE")
        except sqlite3.OperationalError:
            pass  # Coluna já existe
        
        # Tabela de DVDs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dvds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sinopse TEXT,
            ano_lancamento INTEGER,
            ano_aquisicao INTEGER,
            disponivel INTEGER DEFAULT 1
        )
        """)
        
        # Tabela de Aluguéis
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alugueis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_aluguel TEXT NOT NULL,
            cliente_id INTEGER NOT NULL,
            data_devolucao TEXT,
            devolvido INTEGER DEFAULT 0,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
        """)
        
        # Tabela de relação entre Aluguéis e DVDs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS aluguel_dvd (
            aluguel_id INTEGER,
            dvd_id INTEGER,
            PRIMARY KEY (aluguel_id, dvd_id),
            FOREIGN KEY (aluguel_id) REFERENCES alugueis (id),
            FOREIGN KEY (dvd_id) REFERENCES dvds (id)
        )
        """)
        
        conn.commit()
        conn.close()