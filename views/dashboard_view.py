from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QGroupBox, QGridLayout, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from controllers.aluguel_controller import AluguelController
from controllers.cliente_controller import ClienteController
from controllers.dvd_controller import DVDController
from database.aluguel_dao import AluguelDAO
from datetime import datetime, timedelta
import sqlite3
from database.config import DatabaseConfig

class DashboardView(QWidget):
    """View para exibir dashboard com estatísticas da locadora."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.carregar_dados()
    
    def init_ui(self):
        """Inicializa a interface do usuário."""
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Dashboard - Estatísticas da Locadora")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Layout horizontal para as seções principais
        main_layout = QHBoxLayout()
        
        # Coluna esquerda - Filmes mais alugados
        left_column = QVBoxLayout()
        
        # Filmes mais alugados
        filmes_group = QGroupBox("Top 10 - Filmes Mais Alugados")
        filmes_layout = QVBoxLayout()
        
        self.tabela_filmes = QTableWidget()
        self.tabela_filmes.setColumnCount(3)
        self.tabela_filmes.setHorizontalHeaderLabels(["Filme", "Aluguéis", "Receita (R$)"])
        self.tabela_filmes.setMaximumHeight(300)
        filmes_layout.addWidget(self.tabela_filmes)
        
        filmes_group.setLayout(filmes_layout)
        left_column.addWidget(filmes_group)
        
        # Clientes que mais alugam
        clientes_group = QGroupBox("Top 10 - Clientes que Mais Alugam")
        clientes_layout = QVBoxLayout()
        
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(4)
        self.tabela_clientes.setHorizontalHeaderLabels(["Cliente", "CPF", "Aluguéis", "Valor Total (R$)"])
        self.tabela_clientes.setMaximumHeight(300)
        clientes_layout.addWidget(self.tabela_clientes)
        
        clientes_group.setLayout(clientes_layout)
        left_column.addWidget(clientes_group)
        
        main_layout.addLayout(left_column)
        
        # Coluna direita - Faturamento
        right_column = QVBoxLayout()
        
        # Faturamento por mês
        faturamento_group = QGroupBox("Faturamento - Últimos 3 Meses")
        faturamento_layout = QVBoxLayout()
        
        # Cards de faturamento
        self.cards_layout = QGridLayout()
        faturamento_layout.addLayout(self.cards_layout)
        
        # Tabela detalhada de faturamento
        self.tabela_faturamento = QTableWidget()
        self.tabela_faturamento.setColumnCount(4)
        self.tabela_faturamento.setHorizontalHeaderLabels(["Mês", "Aluguéis", "Receita (R$)", "Ticket Médio (R$)"])
        self.tabela_faturamento.setMaximumHeight(200)
        faturamento_layout.addWidget(self.tabela_faturamento)
        
        faturamento_group.setLayout(faturamento_layout)
        right_column.addWidget(faturamento_group)
        
        # Estatísticas gerais
        stats_group = QGroupBox("Estatísticas Gerais")
        stats_layout = QGridLayout()
        
        self.label_total_clientes = QLabel("Total de Clientes: 0")
        self.label_total_dvds = QLabel("Total de DVDs: 0")
        self.label_total_alugueis = QLabel("Total de Aluguéis: 0")
        self.label_dvds_alugados = QLabel("DVDs Alugados: 0")
        self.label_dvds_disponiveis = QLabel("DVDs Disponíveis: 0")
        self.label_alugueis_atraso = QLabel("Aluguéis em Atraso: 0")
        
        stats_layout.addWidget(self.label_total_clientes, 0, 0)
        stats_layout.addWidget(self.label_total_dvds, 0, 1)
        stats_layout.addWidget(self.label_total_alugueis, 1, 0)
        stats_layout.addWidget(self.label_dvds_alugados, 1, 1)
        stats_layout.addWidget(self.label_dvds_disponiveis, 2, 0)
        stats_layout.addWidget(self.label_alugueis_atraso, 2, 1)
        
        stats_group.setLayout(stats_layout)
        right_column.addWidget(stats_group)
        
        main_layout.addLayout(right_column)
        layout.addLayout(main_layout)
        
        # Botão de atualizar
        btn_atualizar = QPushButton("🔄 Atualizar Dashboard")
        btn_atualizar.clicked.connect(self.carregar_dados)
        layout.addWidget(btn_atualizar)
        
        self.setLayout(layout)
    
    def carregar_dados(self):
        """Carrega todos os dados do dashboard."""
        self.carregar_filmes_mais_alugados()
        self.carregar_clientes_mais_alugam()
        self.carregar_faturamento_mensal()
        self.carregar_estatisticas_gerais()
    
    def carregar_filmes_mais_alugados(self):
        """Carrega os filmes mais alugados."""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT d.nome, COUNT(ad.dvd_id) as total_alugueis, 
               COUNT(ad.dvd_id) * 5.0 as receita_estimada
        FROM dvds d
        JOIN aluguel_dvd ad ON d.id = ad.dvd_id
        GROUP BY d.id, d.nome
        ORDER BY total_alugueis DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        self.tabela_filmes.setRowCount(len(resultados))
        
        for i, (nome, total_alugueis, receita) in enumerate(resultados):
            self.tabela_filmes.setItem(i, 0, QTableWidgetItem(nome))
            self.tabela_filmes.setItem(i, 1, QTableWidgetItem(str(total_alugueis)))
            self.tabela_filmes.setItem(i, 2, QTableWidgetItem(f"R$ {receita:.2f}"))
        
        self.tabela_filmes.resizeColumnsToContents()
        conn.close()
    
    def carregar_clientes_mais_alugam(self):
        """Carrega os clientes que mais alugam."""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT c.nome, c.cpf, COUNT(a.id) as total_alugueis,
               COUNT(a.id) * 5.0 as valor_total
        FROM clientes c
        JOIN alugueis a ON c.id = a.cliente_id
        GROUP BY c.id, c.nome, c.cpf
        ORDER BY total_alugueis DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        self.tabela_clientes.setRowCount(len(resultados))
        
        for i, (nome, cpf, total_alugueis, valor_total) in enumerate(resultados):
            self.tabela_clientes.setItem(i, 0, QTableWidgetItem(nome))
            self.tabela_clientes.setItem(i, 1, QTableWidgetItem(cpf))
            self.tabela_clientes.setItem(i, 2, QTableWidgetItem(str(total_alugueis)))
            self.tabela_clientes.setItem(i, 3, QTableWidgetItem(f"R$ {valor_total:.2f}"))
        
        self.tabela_clientes.resizeColumnsToContents()
        conn.close()
    
    def carregar_faturamento_mensal(self):
        """Carrega o faturamento dos últimos 3 meses."""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Calcula as datas dos últimos 3 meses
        hoje = datetime.now()
        meses = []
        
        for i in range(3):
            data_mes = hoje - timedelta(days=30 * i)
            inicio_mes = data_mes.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if i == 0:
                fim_mes = hoje
            else:
                proximo_mes = inicio_mes.replace(month=inicio_mes.month + 1) if inicio_mes.month < 12 else inicio_mes.replace(year=inicio_mes.year + 1, month=1)
                fim_mes = proximo_mes - timedelta(days=1)
            
            meses.append((inicio_mes, fim_mes, data_mes.strftime('%B %Y')))
        
        # Limpa cards anteriores
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        self.tabela_faturamento.setRowCount(len(meses))
        
        for i, (inicio, fim, nome_mes) in enumerate(meses):
            query = """
            SELECT COUNT(a.id) as total_alugueis,
                   COUNT(ad.dvd_id) as total_dvds_alugados
            FROM alugueis a
            LEFT JOIN aluguel_dvd ad ON a.id = ad.aluguel_id
            WHERE datetime(a.data_aluguel) BETWEEN ? AND ?
            """
            
            cursor.execute(query, (inicio.isoformat(), fim.isoformat()))
            resultado = cursor.fetchone()
            
            total_alugueis = resultado[0] if resultado[0] else 0
            total_dvds = resultado[1] if resultado[1] else 0
            receita = total_dvds * 5.0  # R$ 5,00 por DVD
            ticket_medio = receita / total_alugueis if total_alugueis > 0 else 0
            
            # Adiciona à tabela
            self.tabela_faturamento.setItem(i, 0, QTableWidgetItem(nome_mes))
            self.tabela_faturamento.setItem(i, 1, QTableWidgetItem(str(total_alugueis)))
            self.tabela_faturamento.setItem(i, 2, QTableWidgetItem(f"R$ {receita:.2f}"))
            self.tabela_faturamento.setItem(i, 3, QTableWidgetItem(f"R$ {ticket_medio:.2f}"))
            
            # Cria card para o mês
            card = self.criar_card_faturamento(nome_mes, total_alugueis, receita)
            self.cards_layout.addWidget(card, i // 2, i % 2)
        
        self.tabela_faturamento.resizeColumnsToContents()
        conn.close()
    
    def criar_card_faturamento(self, mes, alugueis, receita):
        """Cria um card de faturamento para um mês."""
        card = QGroupBox(mes)
        layout = QVBoxLayout()
        
        label_alugueis = QLabel(f"Aluguéis: {alugueis}")
        label_alugueis.setFont(QFont("Arial", 10, QFont.Bold))
        
        label_receita = QLabel(f"Receita: R$ {receita:.2f}")
        label_receita.setFont(QFont("Arial", 12, QFont.Bold))
        label_receita.setStyleSheet("color: green;")
        
        layout.addWidget(label_alugueis)
        layout.addWidget(label_receita)
        
        card.setLayout(layout)
        card.setMaximumHeight(100)
        
        return card
    
    def carregar_estatisticas_gerais(self):
        """Carrega as estatísticas gerais."""
        # Total de clientes
        clientes = ClienteController.listar_clientes()
        self.label_total_clientes.setText(f"Total de Clientes: {len(clientes)}")
        
        # Total de DVDs
        dvds = DVDController.listar_dvds()
        total_dvds = len(dvds)
        dvds_disponiveis = len([dvd for dvd in dvds if dvd.disponivel])
        dvds_alugados = total_dvds - dvds_disponiveis
        
        self.label_total_dvds.setText(f"Total de DVDs: {total_dvds}")
        self.label_dvds_disponiveis.setText(f"DVDs Disponíveis: {dvds_disponiveis}")
        self.label_dvds_alugados.setText(f"DVDs Alugados: {dvds_alugados}")
        
        # Total de aluguéis
        alugueis = AluguelController.listar_alugueis()
        self.label_total_alugueis.setText(f"Total de Aluguéis: {len(alugueis)}")
        
        # Aluguéis em atraso
        alugueis_atraso = AluguelController.listar_alugueis_em_atraso()
        self.label_alugueis_atraso.setText(f"Aluguéis em Atraso: {len(alugueis_atraso)}")