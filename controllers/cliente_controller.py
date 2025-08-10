from models.cliente import Cliente
from database.cliente_dao import ClienteDAO

class ClienteController:
    """Controlador para gerenciar operações relacionadas a clientes."""
    
    @staticmethod
    def cadastrar_cliente(cpf, nome, telefone, endereco):
        """Cadastra um novo cliente.
        
        Args:
            cpf (str): CPF do cliente.
            nome (str): Nome do cliente.
            telefone (str): Telefone do cliente.
            endereco (str): Endereço do cliente.
            
        Returns:
            Cliente: Cliente cadastrado com ID.
        """
        cliente = Cliente(cpf=cpf, nome=nome, telefone=telefone, endereco=endereco)
        cliente.id = ClienteDAO.inserir(cliente)
        return cliente
    
    @staticmethod
    def atualizar_cliente(cliente_id, cpf, nome, telefone, endereco):
        """Atualiza os dados de um cliente existente.
        
        Args:
            cliente_id (int): ID do cliente a ser atualizado.
            cpf (str): Novo CPF do cliente.
            nome (str): Novo nome do cliente.
            telefone (str): Novo telefone do cliente.
            endereco (str): Novo endereço do cliente.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        cliente = Cliente(id=cliente_id, cpf=cpf, nome=nome, telefone=telefone, endereco=endereco)
        return ClienteDAO.atualizar(cliente)
    
    @staticmethod
    def excluir_cliente(cliente_id):
        """Exclui um cliente.
        
        Args:
            cliente_id (int): ID do cliente a ser excluído.
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        return ClienteDAO.excluir(cliente_id)
    
    @staticmethod
    def buscar_cliente(cliente_id):
        """Busca um cliente pelo ID.
        
        Args:
            cliente_id (int): ID do cliente a ser buscado.
            
        Returns:
            Cliente: Cliente encontrado ou None se não encontrado.
        """
        return ClienteDAO.buscar_por_id(cliente_id)
    
    @staticmethod
    def listar_clientes():
        """Lista todos os clientes cadastrados.
        
        Returns:
            list: Lista de objetos Cliente.
        """
        return ClienteDAO.listar_todos()
    
    @staticmethod
    def buscar_clientes_por_nome(nome):
        """Busca clientes pelo nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado.
            
        Returns:
            list: Lista de objetos Cliente que correspondem à busca.
        """
        return ClienteDAO.buscar_por_nome(nome)
    
    @staticmethod
    def buscar_cliente_por_cpf(cpf):
        """Busca um cliente pelo CPF.
        
        Args:
            cpf (str): CPF do cliente a ser buscado.
            
        Returns:
            Cliente: Cliente encontrado ou None se não encontrado.
        """
        return ClienteDAO.buscar_por_cpf(cpf)