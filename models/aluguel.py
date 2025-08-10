from datetime import datetime

class Aluguel:
    """Classe que representa um aluguel de DVDs."""
    
    def __init__(self, id=None, data_aluguel=None, cliente_id=None, dvds_ids=None, data_devolucao=None, devolvido=False):
        """Inicializa um novo aluguel.
        
        Args:
            id (int, optional): ID único do aluguel. Defaults to None.
            data_aluguel (datetime, optional): Data em que o aluguel foi realizado. Defaults to None.
            cliente_id (int, optional): ID do cliente que realizou o aluguel. Defaults to None.
            dvds_ids (list, optional): Lista de IDs dos DVDs alugados. Defaults to None.
            data_devolucao (datetime, optional): Data prevista para devolução. Defaults to None.
            devolvido (bool, optional): Indica se o aluguel foi devolvido. Defaults to False.
        """
        self.id = id
        self.data_aluguel = data_aluguel if data_aluguel else datetime.now()
        self.cliente_id = cliente_id
        self.dvds_ids = dvds_ids if dvds_ids else []
        self.data_devolucao = data_devolucao
        self.devolvido = devolvido
    
    def __str__(self):
        """Retorna uma representação em string do aluguel.
        
        Returns:
            str: Representação em string do aluguel.
        """
        status = "Devolvido" if self.devolvido else "Em aberto"
        return f"Aluguel #{self.id} - {self.data_aluguel.strftime('%d/%m/%Y')} - {status}"
    
    def calcular_atraso(self):
        """Calcula o número de dias de atraso na devolução.
        
        Returns:
            int: Número de dias de atraso (0 se não houver atraso ou se já foi devolvido).
        """
        if self.devolvido or not self.data_devolucao:
            return 0
        
        hoje = datetime.now().date()
        data_devolucao = self.data_devolucao.date()
        
        if hoje > data_devolucao:
            return (hoje - data_devolucao).days
        return 0
    
    def to_dict(self):
        """Converte o objeto Aluguel para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do aluguel.
        """
        return {
            "id": self.id,
            "data_aluguel": self.data_aluguel.isoformat() if self.data_aluguel else None,
            "cliente_id": self.cliente_id,
            "dvds_ids": self.dvds_ids,
            "data_devolucao": self.data_devolucao.isoformat() if self.data_devolucao else None,
            "devolvido": self.devolvido
        }
    
    @staticmethod
    def from_dict(data):
        """Cria um objeto Aluguel a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados do aluguel.
            
        Returns:
            Aluguel: Objeto Aluguel criado.
        """
        data_aluguel = datetime.fromisoformat(data.get("data_aluguel")) if data.get("data_aluguel") else None
        data_devolucao = datetime.fromisoformat(data.get("data_devolucao")) if data.get("data_devolucao") else None
        
        return Aluguel(
            id=data.get("id"),
            data_aluguel=data_aluguel,
            cliente_id=data.get("cliente_id"),
            dvds_ids=data.get("dvds_ids", []),
            data_devolucao=data_devolucao,
            devolvido=data.get("devolvido", False)
        )