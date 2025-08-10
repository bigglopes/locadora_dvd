class Cliente:
    """Classe que representa um cliente da locadora de DVDs."""
    
    def __init__(self, id=None, cpf="", nome="", telefone="", endereco=""):
        """Inicializa um novo cliente.
        
        Args:
            id (int, optional): ID único do cliente. Defaults to None.
            cpf (str, optional): CPF do cliente (chave principal). Defaults to "".
            nome (str, optional): Nome do cliente. Defaults to "".
            telefone (str, optional): Telefone do cliente. Defaults to "".
            endereco (str, optional): Endereço do cliente. Defaults to "".
        """
        self.id = id
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
    
    def __str__(self):
        """Retorna uma representação em string do cliente.
        
        Returns:
            str: Representação em string do cliente.
        """
        return f"{self.nome} - {self.telefone}"
    
    def to_dict(self):
        """Converte o objeto Cliente para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do cliente.
        """
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "telefone": self.telefone,
            "endereco": self.endereco
        }
    
    @staticmethod
    def from_dict(data):
        """Cria um objeto Cliente a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados do cliente.
            
        Returns:
            Cliente: Objeto Cliente criado.
        """
        return Cliente(
            id=data.get("id"),
            cpf=data.get("cpf", ""),
            nome=data.get("nome", ""),
            telefone=data.get("telefone", ""),
            endereco=data.get("endereco", "")
        )