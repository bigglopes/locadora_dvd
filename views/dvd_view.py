from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QGroupBox, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from datetime import datetime

from controllers.dvd_controller import DVDController

class DVDView(QWidget):
    """Interface para gerenciamento de DVDs."""
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.carregar_dvds()
    
    def init_ui(self):
        """Inicializa a interface do usuário."""
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Grupo de cadastro/edição
        form_group = QGroupBox("Cadastro de DVD")
        form_layout = QFormLayout()
        
        # Campos de entrada
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("Automático")
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome/título do DVD")
        
        self.sinopse_input = QLineEdit()
        self.sinopse_input.setPlaceholderText("Sinopse do DVD")
        
        self.ano_lancamento_input = QSpinBox()
        self.ano_lancamento_input.setRange(1900, datetime.now().year)
        self.ano_lancamento_input.setValue(datetime.now().year)
        
        self.ano_aquisicao_input = QSpinBox()
        self.ano_aquisicao_input.setRange(1900, datetime.now().year)
        self.ano_aquisicao_input.setValue(datetime.now().year)
        
        self.disponivel_input = QCheckBox("Disponível para aluguel")
        self.disponivel_input.setChecked(True)
        
        # Adiciona os campos ao layout do formulário
        form_layout.addRow("ID:", self.id_input)
        form_layout.addRow("Nome:", self.nome_input)
        form_layout.addRow("Sinopse:", self.sinopse_input)
        form_layout.addRow("Ano de Lançamento:", self.ano_lancamento_input)
        form_layout.addRow("Ano de Aquisição:", self.ano_aquisicao_input)
        form_layout.addRow("", self.disponivel_input)
        
        form_group.setLayout(form_layout)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        self.novo_btn = QPushButton("Novo")
        self.novo_btn.setIcon(self.style().standardIcon(self.style().SP_FileDialogNewFolder))
        
        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.setIcon(self.style().standardIcon(self.style().SP_DialogSaveButton))
        
        self.excluir_btn = QPushButton("Excluir")
        self.excluir_btn.setIcon(self.style().standardIcon(self.style().SP_TrashIcon))
        
        self.limpar_btn = QPushButton("Limpar")
        self.limpar_btn.setIcon(self.style().standardIcon(self.style().SP_DialogResetButton))
        
        self.atualizar_btn = QPushButton("Atualizar Listagem")
        self.atualizar_btn.setIcon(self.style().standardIcon(self.style().SP_BrowserReload))
        
        button_layout.addWidget(self.novo_btn)
        button_layout.addWidget(self.salvar_btn)
        button_layout.addWidget(self.excluir_btn)
        button_layout.addWidget(self.limpar_btn)
        button_layout.addWidget(self.atualizar_btn)
        
        # Grupo de busca
        search_group = QGroupBox("Buscar DVD")
        search_layout = QHBoxLayout()
        
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("Digite o título ou código do DVD (deixe vazio para listar todos)")
        
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setIcon(self.style().standardIcon(self.style().SP_FileDialogDetailedView))
        
        search_layout.addWidget(QLabel("Título/Código:"))
        search_layout.addWidget(self.busca_input)
        search_layout.addWidget(self.buscar_btn)
        
        search_group.setLayout(search_layout)
        
        # Tabela de DVDs
        self.tabela_dvds = QTableWidget()
        self.tabela_dvds.setColumnCount(6)
        self.tabela_dvds.setHorizontalHeaderLabels(["ID", "Nome", "Sinopse", "Ano Lançamento", "Ano Aquisição", "Disponível"])
        self.tabela_dvds.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Adiciona os widgets ao layout principal
        main_layout.addWidget(form_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(search_group)
        main_layout.addWidget(QLabel("DVDs Cadastrados:"))
        main_layout.addWidget(self.tabela_dvds)
        
        # Define o layout principal
        self.setLayout(main_layout)
        
        # Conecta os sinais
        self.novo_btn.clicked.connect(self.limpar_campos)
        self.salvar_btn.clicked.connect(self.salvar_dvd)
        self.excluir_btn.clicked.connect(self.excluir_dvd)
        self.limpar_btn.clicked.connect(self.limpar_campos)
        self.atualizar_btn.clicked.connect(self.carregar_dvds)
        self.buscar_btn.clicked.connect(self.buscar_dvd)
        self.busca_input.returnPressed.connect(self.buscar_dvd)
        self.tabela_dvds.itemClicked.connect(self.selecionar_dvd)
    
    def buscar_dvd(self):
        """Busca clientes por CPF ou lista todos se CPF estiver vazio."""
        dvd_busca = self.busca_input.text().strip()
        
        self.tabela_dvds.setRowCount(0)
        
        if dvd_busca:
            # Busca por ID específico
            dvd = DVDController.buscar_dvd(dvd_busca)
            
            if dvd:
                row = self.tabela_dvds.rowCount()
                self.tabela_dvds.insertRow(row)
                
                self.tabela_dvds.setItem(row, 0, QTableWidgetItem(str(dvd.id)))
                self.tabela_dvds.setItem(row, 1, QTableWidgetItem(dvd.nome))
                self.tabela_dvds.setItem(row, 2, QTableWidgetItem(dvd.sinopse))
                self.tabela_dvds.setItem(row, 3, QTableWidgetItem(str(dvd.ano_lancamento) if dvd.ano_lancamento else ""))
                self.tabela_dvds.setItem(row, 4, QTableWidgetItem(str(dvd.ano_aquisicao) if dvd.ano_aquisicao else ""))
                self.tabela_dvds.setItem(row, 5, QTableWidgetItem("Sim" if dvd.disponivel else "Não"))
            else:
                QMessageBox.information(self, "Resultado", "Nenhum dvd encontrado com este titulo.")
        else:
            # Lista todos os clientes
            self.carregar_dvds()
   
    def carregar_dvds(self):
        """Carrega a lista de DVDs na tabela."""
        self.tabela_dvds.setRowCount(0)
        
        dvds = DVDController.listar_dvds()
        
        for dvd in dvds:
            row = self.tabela_dvds.rowCount()
            self.tabela_dvds.insertRow(row)
            
            self.tabela_dvds.setItem(row, 0, QTableWidgetItem(str(dvd.id)))
            self.tabela_dvds.setItem(row, 1, QTableWidgetItem(dvd.nome))
            self.tabela_dvds.setItem(row, 2, QTableWidgetItem(dvd.sinopse))
            self.tabela_dvds.setItem(row, 3, QTableWidgetItem(str(dvd.ano_lancamento) if dvd.ano_lancamento else ""))
            self.tabela_dvds.setItem(row, 4, QTableWidgetItem(str(dvd.ano_aquisicao) if dvd.ano_aquisicao else ""))
            self.tabela_dvds.setItem(row, 5, QTableWidgetItem("Sim" if dvd.disponivel else "Não"))
    
    def limpar_campos(self):
        """Limpa os campos de entrada."""
        self.id_input.clear()
        self.nome_input.clear()
        self.sinopse_input.clear()
        self.ano_lancamento_input.setValue(datetime.now().year)
        self.ano_aquisicao_input.setValue(datetime.now().year)
        self.disponivel_input.setChecked(True)
        self.nome_input.setFocus()
    
    def salvar_dvd(self):
        """Salva um DVD (novo ou existente)."""
        nome = self.nome_input.text().strip()
        sinopse = self.sinopse_input.text().strip()
        ano_lancamento = self.ano_lancamento_input.value()
        ano_aquisicao = self.ano_aquisicao_input.value()
        disponivel = self.disponivel_input.isChecked()
        
        if not nome:
            QMessageBox.warning(self, "Aviso", "O nome do DVD é obrigatório.")
            self.nome_input.setFocus()
            return
        
        dvd_id = self.id_input.text()
        
        if dvd_id:  # Atualização
            sucesso = DVDController.atualizar_dvd(
                int(dvd_id), nome, sinopse, ano_lancamento, ano_aquisicao, disponivel
            )
            mensagem = "DVD atualizado com sucesso!" if sucesso else "Erro ao atualizar DVD."
        else:  # Novo cadastro
            dvd = DVDController.cadastrar_dvd(nome, sinopse, ano_lancamento, ano_aquisicao)
            sucesso = dvd is not None
            mensagem = "DVD cadastrado com sucesso!" if sucesso else "Erro ao cadastrar DVD."
        
        if sucesso:
            self.limpar_campos()
            self.carregar_dvds()
            QMessageBox.information(self, "Sucesso", mensagem)
        else:
            QMessageBox.critical(self, "Erro", mensagem)
    
    def excluir_dvd(self):
        """Exclui um DVD selecionado."""
        dvd_id = self.id_input.text()
        
        if not dvd_id:
            QMessageBox.warning(self, "Aviso", "Selecione um DVD para excluir.")
            return
        
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            "Tem certeza que deseja excluir este DVD?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            sucesso = DVDController.excluir_dvd(int(dvd_id))
            
            if sucesso:
                self.limpar_campos()
                self.carregar_dvds()
                QMessageBox.information(self, "Sucesso", "DVD excluído com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir DVD.")
    
    def selecionar_dvd(self, item):
        """Seleciona um DVD da tabela para edição.
        
        Args:
            item (QTableWidgetItem): Item clicado na tabela.
        """
        row = item.row()
        
        dvd_id = self.tabela_dvds.item(row, 0).text()
        nome = self.tabela_dvds.item(row, 1).text()
        sinopse = self.tabela_dvds.item(row, 2).text()
        
        ano_lancamento_text = self.tabela_dvds.item(row, 3).text()
        ano_lancamento = int(ano_lancamento_text) if ano_lancamento_text else datetime.now().year
        
        ano_aquisicao_text = self.tabela_dvds.item(row, 4).text()
        ano_aquisicao = int(ano_aquisicao_text) if ano_aquisicao_text else datetime.now().year
        
        disponivel = self.tabela_dvds.item(row, 5).text() == "Sim"
        
        self.id_input.setText(dvd_id)
        self.nome_input.setText(nome)
        self.sinopse_input.setText(sinopse)
        self.ano_lancamento_input.setValue(ano_lancamento)
        self.ano_aquisicao_input.setValue(ano_aquisicao)
        self.disponivel_input.setChecked(disponivel)