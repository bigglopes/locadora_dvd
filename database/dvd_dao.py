from database.config import DatabaseConfig
from models.dvd import DVD

class DVDDAO:
    """Data Access Object para a entidade DVD."""
    
    @staticmethod
    def inserir(dvd):
        """Insere um novo DVD no banco de dados.
        
        Args:
            dvd (DVD): Objeto DVD a ser inserido.
            
        Returns:
            int: ID do DVD inserido.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO dvds (nome, sinopse, ano_lancamento, ano_aquisicao, disponivel)
        VALUES (?, ?, ?, ?, ?)
        """, (dvd.nome, dvd.sinopse, dvd.ano_lancamento, dvd.ano_aquisicao, 1 if dvd.disponivel else 0))
        
        dvd.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return dvd.id
    
    @staticmethod
    def atualizar(dvd):
        """Atualiza um DVD existente no banco de dados.
        
        Args:
            dvd (DVD): Objeto DVD com os dados atualizados.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE dvds
        SET nome = ?, sinopse = ?, ano_lancamento = ?, ano_aquisicao = ?, disponivel = ?
        WHERE id = ?
        """, (dvd.nome, dvd.sinopse, dvd.ano_lancamento, dvd.ano_aquisicao, 1 if dvd.disponivel else 0, dvd.id))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def excluir(dvd_id):
        """Exclui um DVD do banco de dados.
        
        Args:
            dvd_id (int): ID do DVD a ser excluído.
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM dvds WHERE id = ?", (dvd_id,))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def buscar_por_id(dvd_id):
        """Busca um DVD pelo ID.
        
        Args:
            dvd_id (int): ID do DVD a ser buscado.
            
        Returns:
            DVD: Objeto DVD encontrado ou None se não encontrado.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM dvds WHERE id = ?", (dvd_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return DVD(
                id=row["id"],
                nome=row["nome"],
                sinopse=row["sinopse"],
                ano_lancamento=row["ano_lancamento"],
                ano_aquisicao=row["ano_aquisicao"],
                disponivel=bool(row["disponivel"])
            )
        
        return None
    
    @staticmethod
    def listar_todos():
        """Lista todos os DVDs cadastrados.
        
        Returns:
            list: Lista de objetos DVD.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM dvds ORDER BY nome")
        rows = cursor.fetchall()
        
        conn.close()
        
        dvds = []
        for row in rows:
            dvd = DVD(
                id=row["id"],
                nome=row["nome"],
                sinopse=row["sinopse"],
                ano_lancamento=row["ano_lancamento"],
                ano_aquisicao=row["ano_aquisicao"],
                disponivel=bool(row["disponivel"])
            )
            dvds.append(dvd)
        
        return dvds
    
    @staticmethod
    def buscar_por_nome(nome):
        """Busca DVDs pelo nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado.
            
        Returns:
            list: Lista de objetos DVD que correspondem à busca.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM dvds WHERE nome LIKE ? ORDER BY nome", (f"%{nome}%",))
        rows = cursor.fetchall()
        
        conn.close()
        
        dvds = []
        for row in rows:
            dvd = DVD(
                id=row["id"],
                nome=row["nome"],
                sinopse=row["sinopse"],
                ano_lancamento=row["ano_lancamento"],
                ano_aquisicao=row["ano_aquisicao"],
                disponivel=bool(row["disponivel"])
            )
            dvds.append(dvd)
        
        return dvds
    
    @staticmethod
    def listar_disponiveis():
        """Lista todos os DVDs disponíveis para aluguel.
        
        Returns:
            list: Lista de objetos DVD disponíveis.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM dvds WHERE disponivel = 1 ORDER BY nome")
        rows = cursor.fetchall()
        
        conn.close()
        
        dvds = []
        for row in rows:
            dvd = DVD(
                id=row["id"],
                nome=row["nome"],
                sinopse=row["sinopse"],
                ano_lancamento=row["ano_lancamento"],
                ano_aquisicao=row["ano_aquisicao"],
                disponivel=True
            )
            dvds.append(dvd)
        
        return dvds
    
    @staticmethod
    def atualizar_disponibilidade(dvd_id, disponivel):
        """Atualiza a disponibilidade de um DVD.
        
        Args:
            dvd_id (int): ID do DVD.
            disponivel (bool): Nova disponibilidade do DVD.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE dvds
        SET disponivel = ?
        WHERE id = ?
        """, (1 if disponivel else 0, dvd_id))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success