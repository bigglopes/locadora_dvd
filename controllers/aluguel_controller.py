from models.aluguel import Aluguel
from database.aluguel_dao import AluguelDAO
from database.dvd_dao import DVDDAO
from datetime import datetime, timedelta

class AluguelController:
    """Controlador para gerenciar operações relacionadas a aluguéis."""
    
    @staticmethod
    def registrar_aluguel(cliente_id, dvds_ids, dias_para_devolucao=7):
        """Registra um novo aluguel.
        
        Args:
            cliente_id (int): ID do cliente que está alugando.
            dvds_ids (list): Lista de IDs dos DVDs sendo alugados.
            dias_para_devolucao (int, optional): Número de dias para devolução. Defaults to 7.
            
        Returns:
            Aluguel: Aluguel registrado com ID ou None se algum DVD não estiver disponível.
        """
        # Verifica se todos os DVDs estão disponíveis
        for dvd_id in dvds_ids:
            dvd = DVDDAO.buscar_por_id(dvd_id)
            if not dvd or not dvd.disponivel:
                return None
        
        # Cria o aluguel
        data_aluguel = datetime.now()
        data_devolucao = data_aluguel + timedelta(days=dias_para_devolucao)
        
        aluguel = Aluguel(
            data_aluguel=data_aluguel,
            cliente_id=cliente_id,
            dvds_ids=dvds_ids,
            data_devolucao=data_devolucao,
            devolvido=False
        )
        
        aluguel.id = AluguelDAO.inserir(aluguel)
        return aluguel
    
    @staticmethod
    def registrar_devolucao(aluguel_id):
        """Registra a devolução de um aluguel.
        
        Args:
            aluguel_id (int): ID do aluguel a ser devolvido.
            
        Returns:
            bool: True se a devolução foi registrada com sucesso, False caso contrário.
        """
        return AluguelDAO.registrar_devolucao(aluguel_id)
    
    @staticmethod
    def buscar_aluguel(aluguel_id):
        """Busca um aluguel pelo ID.
        
        Args:
            aluguel_id (int): ID do aluguel a ser buscado.
            
        Returns:
            Aluguel: Aluguel encontrado ou None se não encontrado.
        """
        return AluguelDAO.buscar_por_id(aluguel_id)
    
    @staticmethod
    def listar_alugueis():
        """Lista todos os aluguéis cadastrados.
        
        Returns:
            list: Lista de objetos Aluguel.
        """
        return AluguelDAO.listar_todos()
    
    @staticmethod
    def listar_alugueis_cliente(cliente_id):
        """Lista todos os aluguéis de um cliente.
        
        Args:
            cliente_id (int): ID do cliente.
            
        Returns:
            list: Lista de objetos Aluguel do cliente.
        """
        return AluguelDAO.listar_por_cliente(cliente_id)
    
    @staticmethod
    def listar_alugueis_em_atraso():
        """Lista todos os aluguéis em atraso (não devolvidos e com data de devolução vencida).
        
        Returns:
            list: Lista de objetos Aluguel em atraso.
        """
        return AluguelDAO.listar_alugueis_em_atraso()
    
    @staticmethod
    def calcular_valor_aluguel(aluguel_id, valor_diaria=5.0, multa_por_dia_atraso=2.0):
        """Calcula o valor de um aluguel, incluindo possíveis multas por atraso.
        
        Args:
            aluguel_id (int): ID do aluguel.
            valor_diaria (float, optional): Valor da diária por DVD. Defaults to 5.0.
            multa_por_dia_atraso (float, optional): Valor da multa por dia de atraso. Defaults to 2.0.
            
        Returns:
            dict: Dicionário com os valores calculados ou None se o aluguel não for encontrado.
        """
        aluguel = AluguelDAO.buscar_por_id(aluguel_id)
        if not aluguel:
            return None
        
        # Calcula o número de dias do aluguel
        if aluguel.devolvido:
            # Se já foi devolvido, considera a data atual como a data de devolução
            dias = 7  # Valor padrão para aluguéis já devolvidos
        else:
            # Se não foi devolvido, calcula com base na data atual
            data_aluguel = aluguel.data_aluguel.date()
            hoje = datetime.now().date()
            dias = (hoje - data_aluguel).days
            if dias < 1:
                dias = 1
        
        # Calcula o valor base (quantidade de DVDs * valor da diária * dias)
        qtd_dvds = len(aluguel.dvds_ids)
        valor_base = qtd_dvds * valor_diaria * dias
        
        # Calcula a multa por atraso, se houver
        dias_atraso = aluguel.calcular_atraso()
        valor_multa = dias_atraso * multa_por_dia_atraso * qtd_dvds
        
        # Calcula o valor total
        valor_total = valor_base + valor_multa
        
        return {
            "valor_base": valor_base,
            "dias": dias,
            "qtd_dvds": qtd_dvds,
            "dias_atraso": dias_atraso,
            "valor_multa": valor_multa,
            "valor_total": valor_total
        }