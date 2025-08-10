from database.config import DatabaseConfig
from models.aluguel import Aluguel
from datetime import datetime

class AluguelDAO:
    """Data Access Object para a entidade Aluguel."""
    
    @staticmethod
    def inserir(aluguel):
        """Insere um novo aluguel no banco de dados.
        
        Args:
            aluguel (Aluguel): Objeto Aluguel a ser inserido.
            
        Returns:
            int: ID do aluguel inserido.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Insere o aluguel
        cursor.execute("""
        INSERT INTO alugueis (data_aluguel, cliente_id, data_devolucao, devolvido)
        VALUES (?, ?, ?, ?)
        """, (
            aluguel.data_aluguel.isoformat(),
            aluguel.cliente_id,
            aluguel.data_devolucao.isoformat() if aluguel.data_devolucao else None,
            1 if aluguel.devolvido else 0
        ))
        
        aluguel.id = cursor.lastrowid
        
        # Insere os DVDs do aluguel
        for dvd_id in aluguel.dvds_ids:
            cursor.execute("""
            INSERT INTO aluguel_dvd (aluguel_id, dvd_id)
            VALUES (?, ?)
            """, (aluguel.id, dvd_id))
            
            # Atualiza a disponibilidade do DVD
            cursor.execute("""
            UPDATE dvds
            SET disponivel = 0
            WHERE id = ?
            """, (dvd_id,))
        
        conn.commit()
        conn.close()
        
        return aluguel.id
    
    @staticmethod
    def atualizar(aluguel):
        """Atualiza um aluguel existente no banco de dados.
        
        Args:
            aluguel (Aluguel): Objeto Aluguel com os dados atualizados.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE alugueis
        SET data_aluguel = ?, cliente_id = ?, data_devolucao = ?, devolvido = ?
        WHERE id = ?
        """, (
            aluguel.data_aluguel.isoformat(),
            aluguel.cliente_id,
            aluguel.data_devolucao.isoformat() if aluguel.data_devolucao else None,
            1 if aluguel.devolvido else 0,
            aluguel.id
        ))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def excluir(aluguel_id):
        """Exclui um aluguel do banco de dados.
        
        Args:
            aluguel_id (int): ID do aluguel a ser excluído.
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Obtém os DVDs do aluguel
        cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
        dvd_ids = [row["dvd_id"] for row in cursor.fetchall()]
        
        # Exclui as relações com DVDs
        cursor.execute("DELETE FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
        
        # Exclui o aluguel
        cursor.execute("DELETE FROM alugueis WHERE id = ?", (aluguel_id,))
        
        success = cursor.rowcount > 0
        
        # Se a exclusão foi bem-sucedida, atualiza a disponibilidade dos DVDs
        if success:
            for dvd_id in dvd_ids:
                cursor.execute("""
                UPDATE dvds
                SET disponivel = 1
                WHERE id = ?
                """, (dvd_id,))
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def buscar_por_id(aluguel_id):
        """Busca um aluguel pelo ID.
        
        Args:
            aluguel_id (int): ID do aluguel a ser buscado.
            
        Returns:
            Aluguel: Objeto Aluguel encontrado ou None se não encontrado.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM alugueis WHERE id = ?", (aluguel_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Busca os DVDs do aluguel
        cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
        dvd_ids = [row["dvd_id"] for row in cursor.fetchall()]
        
        conn.close()
        
        return Aluguel(
            id=row["id"],
            data_aluguel=datetime.fromisoformat(row["data_aluguel"]),
            cliente_id=row["cliente_id"],
            dvds_ids=dvd_ids,
            data_devolucao=datetime.fromisoformat(row["data_devolucao"]) if row["data_devolucao"] else None,
            devolvido=bool(row["devolvido"])
        )
    
    @staticmethod
    def listar_todos():
        """Lista todos os aluguéis cadastrados.
        
        Returns:
            list: Lista de objetos Aluguel.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM alugueis ORDER BY data_aluguel DESC")
        rows = cursor.fetchall()
        
        alugueis = []
        for row in rows:
            aluguel_id = row["id"]
            
            # Busca os DVDs do aluguel
            cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
            dvd_ids = [r["dvd_id"] for r in cursor.fetchall()]
            
            aluguel = Aluguel(
                id=aluguel_id,
                data_aluguel=datetime.fromisoformat(row["data_aluguel"]),
                cliente_id=row["cliente_id"],
                dvds_ids=dvd_ids,
                data_devolucao=datetime.fromisoformat(row["data_devolucao"]) if row["data_devolucao"] else None,
                devolvido=bool(row["devolvido"])
            )
            alugueis.append(aluguel)
        
        conn.close()
        
        return alugueis
    
    @staticmethod
    def listar_por_cliente(cliente_id):
        """Lista todos os aluguéis de um cliente.
        
        Args:
            cliente_id (int): ID do cliente.
            
        Returns:
            list: Lista de objetos Aluguel do cliente.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM alugueis 
        WHERE cliente_id = ? 
        ORDER BY data_aluguel DESC
        """, (cliente_id,))
        rows = cursor.fetchall()
        
        alugueis = []
        for row in rows:
            aluguel_id = row["id"]
            
            # Busca os DVDs do aluguel
            cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
            dvd_ids = [r["dvd_id"] for r in cursor.fetchall()]
            
            aluguel = Aluguel(
                id=aluguel_id,
                data_aluguel=datetime.fromisoformat(row["data_aluguel"]),
                cliente_id=row["cliente_id"],
                dvds_ids=dvd_ids,
                data_devolucao=datetime.fromisoformat(row["data_devolucao"]) if row["data_devolucao"] else None,
                devolvido=bool(row["devolvido"])
            )
            alugueis.append(aluguel)
        
        conn.close()
        
        return alugueis
    
    @staticmethod
    def registrar_devolucao(aluguel_id):
        """Registra a devolução de um aluguel.
        
        Args:
            aluguel_id (int): ID do aluguel a ser devolvido.
            
        Returns:
            bool: True se a devolução foi registrada com sucesso, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Atualiza o status do aluguel
        cursor.execute("""
        UPDATE alugueis
        SET devolvido = 1
        WHERE id = ?
        """, (aluguel_id,))
        
        success = cursor.rowcount > 0
        
        if success:
            # Obtém os DVDs do aluguel
            cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
            dvd_ids = [row["dvd_id"] for row in cursor.fetchall()]
            
            # Atualiza a disponibilidade dos DVDs
            for dvd_id in dvd_ids:
                cursor.execute("""
                UPDATE dvds
                SET disponivel = 1
                WHERE id = ?
                """, (dvd_id,))
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def listar_alugueis_em_atraso():
        """Lista todos os aluguéis em atraso (não devolvidos e com data de devolução vencida).
        
        Returns:
            list: Lista de objetos Aluguel em atraso.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        hoje = datetime.now().date().isoformat()
        
        cursor.execute("""
        SELECT * FROM alugueis 
        WHERE devolvido = 0 AND data_devolucao < ? 
        ORDER BY data_devolucao
        """, (hoje,))
        rows = cursor.fetchall()
        
        alugueis = []
        for row in rows:
            aluguel_id = row["id"]
            
            # Busca os DVDs do aluguel
            cursor.execute("SELECT dvd_id FROM aluguel_dvd WHERE aluguel_id = ?", (aluguel_id,))
            dvd_ids = [r["dvd_id"] for r in cursor.fetchall()]
            
            aluguel = Aluguel(
                id=aluguel_id,
                data_aluguel=datetime.fromisoformat(row["data_aluguel"]),
                cliente_id=row["cliente_id"],
                dvds_ids=dvd_ids,
                data_devolucao=datetime.fromisoformat(row["data_devolucao"]) if row["data_devolucao"] else None,
                devolvido=False
            )
            alugueis.append(aluguel)
        
        conn.close()
        
        return alugueis