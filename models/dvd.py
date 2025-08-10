class DVD:
    """Classe que representa um DVD na locadora."""
    
    def __init__(self, id=None, nome="", sinopse="", ano_lancamento=None, ano_aquisicao=None, disponivel=True):
        """Inicializa um novo DVD.
        
        Args:
            id (int, optional): ID único do DVD. Defaults to None.
            nome (str, optional): Nome/título do DVD. Defaults to "".
            sinopse (str, optional): Sinopse do DVD. Defaults to "".
            ano_lancamento (int, optional): Ano de lançamento do DVD. Defaults to None.
            ano_aquisicao (int, optional): Ano em que o DVD foi adquirido pela locadora. Defaults to None.
            disponivel (bool, optional): Indica se o DVD está disponível para aluguel. Defaults to True.
        """
        self.id = id
        self.nome = nome
        self.sinopse = sinopse
        self.ano_lancamento = ano_lancamento
        self.ano_aquisicao = ano_aquisicao
        self.disponivel = disponivel
    
    def __str__(self):
        """Retorna uma representação em string do DVD.
        
        Returns:
            str: Representação em string do DVD.
        """
        status = "Disponível" if self.disponivel else "Alugado"
        return f"{self.nome} ({self.ano_lancamento}) - {status}"
    
    def to_dict(self):
        """Converte o objeto DVD para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do DVD.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "sinopse": self.sinopse,
            "ano_lancamento": self.ano_lancamento,
            "ano_aquisicao": self.ano_aquisicao,
            "disponivel": self.disponivel
        }
    
    @staticmethod
    def from_dict(data):
        """Cria um objeto DVD a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados do DVD.
            
        Returns:
            DVD: Objeto DVD criado.
        """
        return DVD(
            id=data.get("id"),
            nome=data.get("nome", ""),
            sinopse=data.get("sinopse", ""),
            ano_lancamento=data.get("ano_lancamento"),
            ano_aquisicao=data.get("ano_aquisicao"),
            disponivel=data.get("disponivel", True)
        )