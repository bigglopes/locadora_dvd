from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QGroupBox, QDateEdit, QComboBox,
                             QListWidget, QListWidgetItem, QSplitter, QSpinBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta

from controllers.aluguel_controller import AluguelController
from controllers.cliente_controller import ClienteController
from controllers.dvd_controller import DVDController

class AluguelView(QWidget):
    """Interface para gerenciamento de aluguéis."""
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.carregar_alugueis()
    
    def init_ui(self):
        """Inicializa a interface do usuário."""
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Splitter para dividir a tela
        splitter = QSplitter(Qt.Vertical)
        
        # Painel superior (cadastro)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # Grupo de cadastro/edição
        form_group = QGroupBox("Novo Aluguel")
        form_layout = QFormLayout()
        
        # Campos de entrada
        self.cliente_combo = QComboBox()
        self.atualizar_combo_clientes()
        
        self.data_aluguel_input = QDateEdit()
        self.data_aluguel_input.setDate(QDate.currentDate())
        self.data_aluguel_input.setCalendarPopup(True)
        
        self.dias_devolucao_input = QSpinBox()
        self.dias_devolucao_input.setRange(1, 30)
        self.dias_devolucao_input.setValue(7)
        
        self.data_devolucao_input = QDateEdit()
        self.data_devolucao_input.setDate(QDate.currentDate().addDays(7))
        self.data_devolucao_input.setCalendarPopup(True)
        self.data_devolucao_input.setReadOnly(True)
        
        # Atualiza a data de devolução quando o número de dias muda
        self.dias_devolucao_input.valueChanged.connect(self.atualizar_data_devolucao)
        
        # Lista de DVDs disponíveis
        self.dvd_combo = QComboBox()
        self.atualizar_combo_dvds()
        
        self.adicionar_dvd_btn = QPushButton("Adicionar DVD")
        self.adicionar_dvd_btn.setIcon(self.style().standardIcon(self.style().SP_ArrowRight))
        dvd_layout = QHBoxLayout()
        dvd_layout.addWidget(self.dvd_combo)
        dvd_layout.addWidget(self.adicionar_dvd_btn)
        
        # Lista de DVDs selecionados
        self.dvds_selecionados_list = QListWidget()
        self.remover_dvd_btn = QPushButton("Remover DVD Selecionado")
        self.remover_dvd_btn.setIcon(self.style().standardIcon(self.style().SP_ArrowLeft))
        
        # Adiciona os campos ao layout do formulário
        form_layout.addRow("Cliente:", self.cliente_combo)
        form_layout.addRow("Data de Aluguel:", self.data_aluguel_input)
        form_layout.addRow("Dias para Devolução:", self.dias_devolucao_input)
        form_layout.addRow("Data de Devolução:", self.data_devolucao_input)
        form_layout.addRow("DVD:", dvd_layout)
        form_layout.addRow("DVDs Selecionados:", self.dvds_selecionados_list)
        form_layout.addRow("", self.remover_dvd_btn)
        
        form_group.setLayout(form_layout)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        self.registrar_btn = QPushButton("Registrar Aluguel")
        self.registrar_btn.setIcon(self.style().standardIcon(self.style().SP_DialogApplyButton))
        
        self.limpar_btn = QPushButton("Limpar")
        self.limpar_btn.setIcon(self.style().standardIcon(self.style().SP_DialogResetButton))
        
        button_layout.addWidget(self.registrar_btn)
        button_layout.addWidget(self.limpar_btn)
        
        # Adiciona os widgets ao layout superior
        top_layout.addWidget(form_group)
        top_layout.addLayout(button_layout)
        
        # Painel inferior (listagem e devolução)
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        # Filtro por nome do cliente
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Filtrar por Cliente:"))
        
        self.filtro_cliente_input = QLineEdit()
        self.filtro_cliente_input.setPlaceholderText("Digite o nome do cliente para filtrar...")
        self.filtro_cliente_input.textChanged.connect(self.filtrar_alugueis)
        filtro_layout.addWidget(self.filtro_cliente_input)
        
        self.limpar_filtro_btn = QPushButton("Limpar Filtro")
        self.limpar_filtro_btn.setIcon(self.style().standardIcon(self.style().SP_DialogResetButton))
        self.limpar_filtro_btn.clicked.connect(self.limpar_filtro)
        filtro_layout.addWidget(self.limpar_filtro_btn)
        
        # Tabela de aluguéis
        self.tabela_alugueis = QTableWidget()
        self.tabela_alugueis.setColumnCount(6)
        self.tabela_alugueis.setHorizontalHeaderLabels(["ID", "Data Aluguel", "Cliente", "DVDs", "Data Devolução", "Status"])
        self.tabela_alugueis.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Botão de devolução
        self.devolver_btn = QPushButton("Registrar Devolução")
        self.devolver_btn.setIcon(self.style().standardIcon(self.style().SP_DialogOkButton))
        
        # Adiciona os widgets ao layout inferior
        bottom_layout.addWidget(QLabel("Aluguéis Registrados:"))
        bottom_layout.addLayout(filtro_layout)
        bottom_layout.addWidget(self.tabela_alugueis)
        bottom_layout.addWidget(self.devolver_btn)
        
        # Adiciona os widgets ao splitter
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        
        # Adiciona o splitter ao layout principal
        main_layout.addWidget(splitter)
        
        # Define o layout principal
        self.setLayout(main_layout)
        
        # Conecta os sinais
        self.adicionar_dvd_btn.clicked.connect(self.adicionar_dvd)
        self.remover_dvd_btn.clicked.connect(self.remover_dvd)
        self.registrar_btn.clicked.connect(self.registrar_aluguel)
        self.limpar_btn.clicked.connect(self.limpar_campos)
        self.devolver_btn.clicked.connect(self.registrar_devolucao)
        self.tabela_alugueis.itemClicked.connect(self.selecionar_aluguel)
    
    def atualizar_combo_clientes(self):
        """Atualiza o combo de clientes."""
        self.cliente_combo.clear()
        
        clientes = ClienteController.listar_clientes()
        
        for cliente in clientes:
            self.cliente_combo.addItem(f"{cliente.nome} ({cliente.telefone})", cliente.id)
    
    def atualizar_combo_dvds(self):
        """Atualiza o combo de DVDs disponíveis."""
        self.dvd_combo.clear()
        
        dvds = DVDController.listar_dvds_disponiveis()
        
        for dvd in dvds:
            self.dvd_combo.addItem(f"{dvd.nome} ({dvd.ano_lancamento})", dvd.id)
    
    def atualizar_data_devolucao(self):
        """Atualiza a data de devolução com base no número de dias."""
        dias = self.dias_devolucao_input.value()
        data_aluguel = self.data_aluguel_input.date().toPyDate()
        data_devolucao = data_aluguel + timedelta(days=dias)
        self.data_devolucao_input.setDate(QDate(data_devolucao.year, data_devolucao.month, data_devolucao.day))
    
    def adicionar_dvd(self):
        """Adiciona um DVD à lista de selecionados."""
        if self.dvd_combo.count() == 0:
            QMessageBox.warning(self, "Aviso", "Não há DVDs disponíveis para aluguel.")
            return
        
        dvd_id = self.dvd_combo.currentData()
        dvd_texto = self.dvd_combo.currentText()
        
        # Verifica se o DVD já está na lista
        for i in range(self.dvds_selecionados_list.count()):
            item = self.dvds_selecionados_list.item(i)
            if item.data(Qt.UserRole) == dvd_id:
                QMessageBox.warning(self, "Aviso", "Este DVD já foi selecionado.")
                return
        
        # Adiciona o DVD à lista
        item = QListWidgetItem(dvd_texto)
        item.setData(Qt.UserRole, dvd_id)
        self.dvds_selecionados_list.addItem(item)
        
        # Remove o DVD do combo
        self.dvd_combo.removeItem(self.dvd_combo.currentIndex())
    
    def remover_dvd(self):
        """Remove um DVD da lista de selecionados."""
        item = self.dvds_selecionados_list.currentItem()
        
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um DVD para remover.")
            return
        
        dvd_id = item.data(Qt.UserRole)
        dvd_texto = item.text()
        
        # Remove o DVD da lista
        row = self.dvds_selecionados_list.row(item)
        self.dvds_selecionados_list.takeItem(row)
        
        # Adiciona o DVD de volta ao combo
        self.dvd_combo.addItem(dvd_texto, dvd_id)
    
    def limpar_campos(self):
        """Limpa os campos de entrada."""
        self.cliente_combo.setCurrentIndex(0 if self.cliente_combo.count() > 0 else -1)
        self.data_aluguel_input.setDate(QDate.currentDate())
        self.dias_devolucao_input.setValue(7)
        self.atualizar_data_devolucao()
        
        # Limpa a lista de DVDs selecionados
        self.dvds_selecionados_list.clear()
        
        # Atualiza o combo de DVDs
        self.atualizar_combo_dvds()
    
    def registrar_aluguel(self):
        """Registra um novo aluguel."""
        if self.cliente_combo.count() == 0:
            QMessageBox.warning(self, "Aviso", "Não há clientes cadastrados.")
            return
        
        if self.dvds_selecionados_list.count() == 0:
            QMessageBox.warning(self, "Aviso", "Selecione pelo menos um DVD para alugar.")
            return
        
        cliente_id = self.cliente_combo.currentData()
        data_aluguel = self.data_aluguel_input.date().toPyDate()
        dias_devolucao = self.dias_devolucao_input.value()
        
        # Obtém a lista de IDs dos DVDs selecionados
        dvds_ids = []
        for i in range(self.dvds_selecionados_list.count()):
            item = self.dvds_selecionados_list.item(i)
            dvds_ids.append(item.data(Qt.UserRole))
        
        # Converte a data para datetime
        data_aluguel_dt = datetime.combine(data_aluguel, datetime.min.time())
        
        # Registra o aluguel
        aluguel = AluguelController.registrar_aluguel(cliente_id, dvds_ids, dias_devolucao)
        
        if aluguel:
            self.limpar_campos()
            self.carregar_alugueis()
            QMessageBox.information(self, "Sucesso", "Aluguel registrado com sucesso!")
        else:
            QMessageBox.critical(self, "Erro", "Erro ao registrar aluguel. Verifique se todos os DVDs estão disponíveis.")
    
    def carregar_alugueis(self, filtro_cliente=None):
        """Carrega a lista de aluguéis na tabela.
        
        Args:
            filtro_cliente (str, optional): Nome do cliente para filtrar. Defaults to None.
        """
        self.tabela_alugueis.setRowCount(0)
        
        alugueis = AluguelController.listar_alugueis()
        
        for aluguel in alugueis:
            # Busca o cliente
            cliente = ClienteController.buscar_cliente(aluguel.cliente_id)
            nome_cliente = cliente.nome if cliente else "Cliente não encontrado"
            
            # Aplica o filtro por nome do cliente se especificado
            if filtro_cliente and filtro_cliente.lower() not in nome_cliente.lower():
                continue
            
            row = self.tabela_alugueis.rowCount()
            self.tabela_alugueis.insertRow(row)
            
            # Busca os DVDs
            dvds_nomes = []
            for dvd_id in aluguel.dvds_ids:
                dvd = DVDController.buscar_dvd(dvd_id)
                if dvd:
                    dvds_nomes.append(dvd.nome)
            
            dvds_texto = ", ".join(dvds_nomes) if dvds_nomes else "Nenhum DVD"
            
            # Formata as datas
            data_aluguel = aluguel.data_aluguel.strftime("%d/%m/%Y") if aluguel.data_aluguel else ""
            data_devolucao = aluguel.data_devolucao.strftime("%d/%m/%Y") if aluguel.data_devolucao else ""
            
            # Define o status
            status = "Devolvido" if aluguel.devolvido else "Em aberto"
            
            # Calcula o atraso
            dias_atraso = aluguel.calcular_atraso()
            if dias_atraso > 0 and not aluguel.devolvido:
                status = f"Em atraso ({dias_atraso} dias)"
            
            # Adiciona os dados à tabela
            self.tabela_alugueis.setItem(row, 0, QTableWidgetItem(str(aluguel.id)))
            self.tabela_alugueis.setItem(row, 1, QTableWidgetItem(data_aluguel))
            self.tabela_alugueis.setItem(row, 2, QTableWidgetItem(nome_cliente))
            self.tabela_alugueis.setItem(row, 3, QTableWidgetItem(dvds_texto))
            self.tabela_alugueis.setItem(row, 4, QTableWidgetItem(data_devolucao))
            self.tabela_alugueis.setItem(row, 5, QTableWidgetItem(status))
            
            # Define a cor da linha de acordo com o status
            if "Em atraso" in status:
                for col in range(self.tabela_alugueis.columnCount()):
                    self.tabela_alugueis.item(row, col).setBackground(Qt.red)
                    self.tabela_alugueis.item(row, col).setForeground(Qt.white)
            elif status == "Devolvido":
                for col in range(self.tabela_alugueis.columnCount()):
                    self.tabela_alugueis.item(row, col).setBackground(Qt.green)
    
    def selecionar_aluguel(self, item):
        """Seleciona um aluguel da tabela.
        
        Args:
            item (QTableWidgetItem): Item clicado na tabela.
        """
        row = item.row()
        aluguel_id = int(self.tabela_alugueis.item(row, 0).text())
        status = self.tabela_alugueis.item(row, 5).text()
        
        # Habilita ou desabilita o botão de devolução
        self.devolver_btn.setEnabled("Devolvido" not in status)
        self.devolver_btn.setProperty("aluguel_id", aluguel_id)
    
    def registrar_devolucao(self):
        """Registra a devolução de um aluguel."""
        aluguel_id = self.devolver_btn.property("aluguel_id")
        
        if not aluguel_id:
            QMessageBox.warning(self, "Aviso", "Selecione um aluguel para registrar a devolução.")
            return
        
        # Calcula o valor do aluguel
        valores = AluguelController.calcular_valor_aluguel(aluguel_id)
        
        if not valores:
            QMessageBox.critical(self, "Erro", "Erro ao calcular o valor do aluguel.")
            return
        
        # Monta a mensagem de confirmação
        mensagem = f"Valor base: R$ {valores['valor_base']:.2f}\n"
        mensagem += f"Quantidade de DVDs: {valores['qtd_dvds']}\n"
        mensagem += f"Dias de aluguel: {valores['dias']}\n"
        
        if valores['dias_atraso'] > 0:
            mensagem += f"Dias de atraso: {valores['dias_atraso']}\n"
            mensagem += f"Valor da multa: R$ {valores['valor_multa']:.2f}\n"
        
        mensagem += f"\nValor total: R$ {valores['valor_total']:.2f}\n\n"
        mensagem += "Confirma a devolução?"
        
        resposta = QMessageBox.question(
            self, "Confirmar Devolução", mensagem,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            sucesso = AluguelController.registrar_devolucao(aluguel_id)
            
            if sucesso:
                self.carregar_alugueis()
                self.atualizar_combo_dvds()
                QMessageBox.information(self, "Sucesso", "Devolução registrada com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao registrar devolução.")
    
    def filtrar_alugueis(self):
        """Filtra os aluguéis pelo nome do cliente."""
        filtro = self.filtro_cliente_input.text().strip()
        self.carregar_alugueis(filtro if filtro else None)
    
    def limpar_filtro(self):
        """Limpa o filtro e recarrega todos os aluguéis."""
        self.filtro_cliente_input.clear()
        self.carregar_alugueis()