from database.config import DatabaseConfig
from models.cliente import Cliente

class ClienteDAO:
    """Data Access Object para a entidade Cliente."""
    
    @staticmethod
    def inserir(cliente):
        """Insere um novo cliente no banco de dados.
        
        Args:
            cliente (Cliente): Objeto Cliente a ser inserido.
            
        Returns:
            int: ID do cliente inserido.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO clientes (cpf, nome, telefone, endereco)
        VALUES (?, ?, ?, ?)
        """, (cliente.cpf, cliente.nome, cliente.telefone, cliente.endereco))
        
        cliente.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return cliente.id
    
    @staticmethod
    def atualizar(cliente):
        """Atualiza um cliente existente no banco de dados.
        
        Args:
            cliente (Cliente): Objeto Cliente com os dados atualizados.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE clientes
        SET cpf = ?, nome = ?, telefone = ?, endereco = ?
        WHERE id = ?
        """, (cliente.cpf, cliente.nome, cliente.telefone, cliente.endereco, cliente.id))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def excluir(cliente_id):
        """Exclui um cliente do banco de dados.
        
        Args:
            cliente_id (int): ID do cliente a ser excluído.
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def buscar_por_id(cliente_id):
        """Busca um cliente pelo ID.
        
        Args:
            cliente_id (int): ID do cliente a ser buscado.
            
        Returns:
            Cliente: Objeto Cliente encontrado ou None se não encontrado.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Cliente(
                id=row["id"],
                cpf=row["cpf"],
                nome=row["nome"],
                telefone=row["telefone"],
                endereco=row["endereco"]
            )
        
        return None
    
    @staticmethod
    def listar_todos():
        """Lista todos os clientes cadastrados.
        
        Returns:
            list: Lista de objetos Cliente.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes ORDER BY nome")
        rows = cursor.fetchall()
        
        conn.close()
        
        clientes = []
        for row in rows:
            cliente = Cliente(
                id=row["id"],
                cpf=row["cpf"],
                nome=row["nome"],
                telefone=row["telefone"],
                endereco=row["endereco"]
            )
            clientes.append(cliente)
        
        return clientes
    
    @staticmethod
    def buscar_por_cpf(cpf):
        """Busca um cliente pelo CPF.
        
        Args:
            cpf (str): CPF do cliente a ser buscado.
            
        Returns:
            Cliente: Objeto Cliente encontrado ou None se não encontrado.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return Cliente(
                id=row["id"],
                cpf=row["cpf"],
                nome=row["nome"],
                telefone=row["telefone"],
                endereco=row["endereco"]
            )
        
        return None
    
    @staticmethod
    def buscar_por_nome(nome):
        """Busca clientes pelo nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado.
            
        Returns:
            list: Lista de objetos Cliente que correspondem à busca.
        """
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes WHERE nome LIKE ? ORDER BY nome", (f"%{nome}%",))
        rows = cursor.fetchall()
        
        conn.close()
        
        clientes = []
        for row in rows:
            cliente = Cliente(
                id=row["id"],
                cpf=row.get("cpf", ""),
                nome=row["nome"],
                telefone=row["telefone"],
                endereco=row["endereco"]
            )
            clientes.append(cliente)

        return clientes