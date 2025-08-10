import sqlite3
import random
from datetime import datetime, timedelta
from database.config import DatabaseConfig
from controllers.cliente_controller import ClienteController
from controllers.dvd_controller import DVDController
from controllers.aluguel_controller import AluguelController

def gerar_cpf():
    """Gera um CPF fictício válido."""
    cpf = [random.randint(0, 9) for _ in range(11)]
    return ''.join(map(str, cpf))

def gerar_nome():
    """Gera um nome fictício."""
    nomes = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos', 'Lucia', 'Paulo', 'Fernanda', 'Ricardo', 'Juliana',
             'Roberto', 'Carla', 'Antonio', 'Patricia', 'José', 'Sandra', 'Francisco', 'Monica', 'Marcos', 'Cristina']
    sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes',
                  'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes', 'Soares', 'Fernandes', 'Vieira', 'Barbosa']
    
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def gerar_telefone():
    """Gera um telefone fictício."""
    return f"({random.randint(11, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"

def gerar_endereco():
    """Gera um endereço fictício."""
    ruas = ['Rua das Flores', 'Av. Principal', 'Rua do Comércio', 'Av. Central', 'Rua da Paz',
            'Rua São João', 'Av. Brasil', 'Rua da Liberdade', 'Rua do Sol', 'Av. Paulista']
    
    return f"{random.choice(ruas)}, {random.randint(1, 999)}"

def criar_clientes(quantidade=200):
    """Cria clientes fictícios."""
    print(f"Criando {quantidade} clientes...")
    clientes_criados = []
    cpfs_usados = set()
    
    for i in range(quantidade):
        # Gera CPF único
        while True:
            cpf = gerar_cpf()
            if cpf not in cpfs_usados:
                cpfs_usados.add(cpf)
                break
        
        nome = gerar_nome()
        telefone = gerar_telefone()
        endereco = gerar_endereco()
        
        try:
            cliente = ClienteController.cadastrar_cliente(cpf, nome, telefone, endereco)
            clientes_criados.append(cliente)
            if (i + 1) % 50 == 0:
                print(f"  {i + 1} clientes criados...")
        except Exception as e:
            print(f"Erro ao criar cliente {i + 1}: {e}")
    
    print(f"Total de {len(clientes_criados)} clientes criados com sucesso!")
    return clientes_criados

def criar_dvds_basicos():
    """Cria uma coleção básica de DVDs se não existirem."""
    dvds_existentes = DVDController.listar_dvds()
    
    if len(dvds_existentes) < 50:
        print("Criando DVDs básicos...")
        
        filmes = [
            ('Matrix', 'Um hacker descobre a realidade', 1999, 2020),
            ('Titanic', 'Romance no navio que afundou', 1997, 2019),
            ('Avatar', 'Mundo alienígena em Pandora', 2009, 2021),
            ('Vingadores', 'Super-heróis salvam o mundo', 2012, 2020),
            ('Jurassic Park', 'Dinossauros voltam à vida', 1993, 2018),
            ('Star Wars', 'Guerra nas estrelas', 1977, 2019),
            ('O Rei Leão', 'Aventura na savana africana', 1994, 2020),
            ('Frozen', 'Princesa com poderes de gelo', 2013, 2021),
            ('Toy Story', 'Brinquedos que ganham vida', 1995, 2019),
            ('Procurando Nemo', 'Peixe-palhaço perdido no oceano', 2003, 2020),
            ('Shrek', 'Ogro verde em aventura', 2001, 2019),
            ('Madagascar', 'Animais do zoológico em aventura', 2005, 2020),
            ('Carros', 'Corrida de carros falantes', 2006, 2021),
            ('Up - Altas Aventuras', 'Casa voadora com balões', 2009, 2020),
            ('Wall-E', 'Robô solitário no espaço', 2008, 2019),
            ('Os Incríveis', 'Família de super-heróis', 2004, 2020),
            ('Monstros S.A.', 'Monstros que assustam crianças', 2001, 2019),
            ('Ratatouille', 'Rato que cozinha', 2007, 2020),
            ('WALL-E', 'Robô apaixonado', 2008, 2021),
            ('Coco', 'Menino no mundo dos mortos', 2017, 2021)
        ]
        
        # Duplicar filmes para ter mais exemplares
        for _ in range(3):
            for nome, sinopse, ano_lancamento, ano_aquisicao in filmes:
                try:
                    DVDController.cadastrar_dvd(nome, sinopse, ano_lancamento, ano_aquisicao)
                except Exception as e:
                    print(f"Erro ao criar DVD {nome}: {e}")
        
        print(f"DVDs criados! Total disponível: {len(DVDController.listar_dvds())}")

def simular_alugueis(clientes, meses=2):
    """Simula aluguéis durante os meses especificados."""
    print(f"Simulando aluguéis por {meses} meses...")
    
    dvds = DVDController.listar_dvds()
    if not dvds:
        print("Nenhum DVD disponível para aluguel!")
        return
    
    data_inicio = datetime.now() - timedelta(days=meses * 30)
    total_alugueis = 0
    
    for dia in range(meses * 30):
        data_atual = data_inicio + timedelta(days=dia)
        
        # Simula entre 5 a 15 aluguéis por dia
        num_alugueis_dia = random.randint(5, 15)
        
        for _ in range(num_alugueis_dia):
            try:
                # Seleciona cliente aleatório
                cliente = random.choice(clientes)
                
                # Seleciona 1-3 DVDs aleatórios
                num_dvds = random.randint(1, 3)
                dvds_selecionados = random.sample(dvds, min(num_dvds, len(dvds)))
                dvd_ids = [dvd.id for dvd in dvds_selecionados]
                
                # Cria aluguel (dias_para_devolucao entre 3 e 10 dias)
                dias_devolucao = random.randint(3, 10)
                aluguel = AluguelController.registrar_aluguel(
                    cliente.id, 
                    dvd_ids, 
                    dias_devolucao
                )
                
                if aluguel:
                    total_alugueis += 1
                    
                    # 70% de chance de devolver o DVD (simula devoluções)
                    if random.random() < 0.7:
                        dias_para_devolucao = random.randint(1, 7)
                        data_devolucao = data_atual + timedelta(days=dias_para_devolucao)
                        
                        if data_devolucao <= datetime.now():
                            AluguelController.registrar_devolucao(aluguel.id)
                            
            except Exception as e:
                print(f"Erro ao criar aluguel: {e}")
        
        if (dia + 1) % 10 == 0:
            print(f"  {dia + 1} dias simulados... ({total_alugueis} aluguéis)")
    
    print(f"Simulação concluída! Total de {total_alugueis} aluguéis criados.")

def main():
    """Função principal para executar a simulação."""
    print("=== SIMULAÇÃO DE DADOS PARA LOCADORA DE DVD ===")
    print("Inicializando banco de dados...")
    
    # Inicializa o banco
    DatabaseConfig.initialize_database()
    
    # Cria DVDs básicos
    criar_dvds_basicos()
    
    # Cria clientes
    clientes = criar_clientes(200)
    
    if clientes:
        # Simula aluguéis
        simular_alugueis(clientes, 2)
    
    print("\n=== SIMULAÇÃO CONCLUÍDA ===")
    print(f"Clientes cadastrados: {len(ClienteController.listar_clientes())}")
    print(f"DVDs disponíveis: {len(DVDController.listar_dvds())}")
    print(f"Aluguéis registrados: {len(AluguelController.listar_alugueis())}")

if __name__ == "__main__":
    main()