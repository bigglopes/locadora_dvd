from models.dvd import DVD
from database.dvd_dao import DVDDAO

class DVDController:
    """Controlador para gerenciar operações relacionadas a DVDs."""
    
    @staticmethod
    def cadastrar_dvd(nome, sinopse, ano_lancamento, ano_aquisicao):
        """Cadastra um novo DVD.
        
        Args:
            nome (str): Nome/título do DVD.
            sinopse (str): Sinopse do DVD.
            ano_lancamento (int): Ano de lançamento do DVD.
            ano_aquisicao (int): Ano em que o DVD foi adquirido pela locadora.
            
        Returns:
            DVD: DVD cadastrado com ID.
        """
        dvd = DVD(
            nome=nome,
            sinopse=sinopse,
            ano_lancamento=ano_lancamento,
            ano_aquisicao=ano_aquisicao,
            disponivel=True
        )
        dvd.id = DVDDAO.inserir(dvd)
        return dvd
    
    @staticmethod
    def atualizar_dvd(dvd_id, nome, sinopse, ano_lancamento, ano_aquisicao, disponivel):
        """Atualiza os dados de um DVD existente.
        
        Args:
            dvd_id (int): ID do DVD a ser atualizado.
            nome (str): Novo nome/título do DVD.
            sinopse (str): Nova sinopse do DVD.
            ano_lancamento (int): Novo ano de lançamento do DVD.
            ano_aquisicao (int): Novo ano de aquisição do DVD.
            disponivel (bool): Nova disponibilidade do DVD.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        dvd = DVD(
            id=dvd_id,
            nome=nome,
            sinopse=sinopse,
            ano_lancamento=ano_lancamento,
            ano_aquisicao=ano_aquisicao,
            disponivel=disponivel
        )
        return DVDDAO.atualizar(dvd)
    
    @staticmethod
    def excluir_dvd(dvd_id):
        """Exclui um DVD.
        
        Args:
            dvd_id (int): ID do DVD a ser excluído.
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        return DVDDAO.excluir(dvd_id)
    
    @staticmethod
    def buscar_dvd(dvd_id):
        """Busca um DVD pelo ID.
        
        Args:
            dvd_id (int): ID do DVD a ser buscado.
            
        Returns:
            DVD: DVD encontrado ou None se não encontrado.
        """
        return DVDDAO.buscar_por_id(dvd_id)
    
    @staticmethod
    def listar_dvds():
        """Lista todos os DVDs cadastrados.
        
        Returns:
            list: Lista de objetos DVD.
        """
        return DVDDAO.listar_todos()
    
    @staticmethod
    def buscar_dvds_por_nome(nome):
        """Busca DVDs pelo nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado.
            
        Returns:
            list: Lista de objetos DVD que correspondem à busca.
        """
        return DVDDAO.buscar_por_nome(nome)
    
    @staticmethod
    def listar_dvds_disponiveis():
        """Lista todos os DVDs disponíveis para aluguel.
        
        Returns:
            list: Lista de objetos DVD disponíveis.
        """
        return DVDDAO.listar_disponiveis()
    
    @staticmethod
    def atualizar_disponibilidade(dvd_id, disponivel):
        """Atualiza a disponibilidade de um DVD.
        
        Args:
            dvd_id (int): ID do DVD.
            disponivel (bool): Nova disponibilidade do DVD.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        return DVDDAO.atualizar_disponibilidade(dvd_id, disponivel)