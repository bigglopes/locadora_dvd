from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from controllers.cliente_controller import ClienteController

class ClienteView(QWidget):
    """Interface para gerenciamento de clientes."""
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.carregar_clientes()
    
    def init_ui(self):
        """Inicializa a interface do usuário."""
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Grupo de cadastro/edição
        form_group = QGroupBox("Cadastro de Cliente")
        form_layout = QFormLayout()
        
        # Campos de entrada
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("Automático")
        
        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("CPF do cliente (somente números)")
        self.cpf_input.setMaxLength(11)
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do cliente")
        
        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("Telefone do cliente")
        
        self.endereco_input = QLineEdit()
        self.endereco_input.setPlaceholderText("Endereço do cliente")
        
        # Adiciona os campos ao layout do formulário
        form_layout.addRow("ID:", self.id_input)
        form_layout.addRow("CPF:", self.cpf_input)
        form_layout.addRow("Nome:", self.nome_input)
        form_layout.addRow("Telefone:", self.telefone_input)
        form_layout.addRow("Endereço:", self.endereco_input)
        
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
        search_group = QGroupBox("Buscar Cliente")
        search_layout = QHBoxLayout()
        
        self.busca_cpf_input = QLineEdit()
        self.busca_cpf_input.setPlaceholderText("Digite o CPF para buscar (deixe vazio para listar todos)")
        self.busca_cpf_input.setMaxLength(11)
        
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setIcon(self.style().standardIcon(self.style().SP_FileDialogDetailedView))
        
        search_layout.addWidget(QLabel("CPF:"))
        search_layout.addWidget(self.busca_cpf_input)
        search_layout.addWidget(self.buscar_btn)
        
        search_group.setLayout(search_layout)
        
        # Tabela de clientes
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(5)
        self.tabela_clientes.setHorizontalHeaderLabels(["ID", "CPF", "Nome", "Telefone", "Endereço"])
        self.tabela_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Adiciona os widgets ao layout principal
        main_layout.addWidget(form_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(search_group)
        main_layout.addWidget(QLabel("Clientes Cadastrados:"))
        main_layout.addWidget(self.tabela_clientes)
        
        # Define o layout principal
        self.setLayout(main_layout)
        
        # Conecta os sinais
        self.novo_btn.clicked.connect(self.limpar_campos)
        self.salvar_btn.clicked.connect(self.salvar_cliente)
        self.excluir_btn.clicked.connect(self.excluir_cliente)
        self.limpar_btn.clicked.connect(self.limpar_campos)
        self.atualizar_btn.clicked.connect(self.carregar_clientes)
        self.buscar_btn.clicked.connect(self.buscar_cliente)
        self.busca_cpf_input.returnPressed.connect(self.buscar_cliente)
        self.tabela_clientes.itemClicked.connect(self.selecionar_cliente)
    
    def carregar_clientes(self):
        """Carrega a lista de clientes na tabela."""
        self.tabela_clientes.setRowCount(0)
        
        clientes = ClienteController.listar_clientes()
        
        for cliente in clientes:
            row = self.tabela_clientes.rowCount()
            self.tabela_clientes.insertRow(row)
            
            self.tabela_clientes.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
            self.tabela_clientes.setItem(row, 1, QTableWidgetItem(cliente.cpf or ""))
            self.tabela_clientes.setItem(row, 2, QTableWidgetItem(cliente.nome))
            self.tabela_clientes.setItem(row, 3, QTableWidgetItem(cliente.telefone))
            self.tabela_clientes.setItem(row, 4, QTableWidgetItem(cliente.endereco))
    
    def limpar_campos(self):
        """Limpa os campos de entrada."""
        self.id_input.clear()
        self.cpf_input.clear()
        self.nome_input.clear()
        self.telefone_input.clear()
        self.endereco_input.clear()
        self.cpf_input.setFocus()
    
    def salvar_cliente(self):
        """Salva um cliente (novo ou existente)."""
        cpf = self.cpf_input.text().strip()
        nome = self.nome_input.text().strip()
        telefone = self.telefone_input.text().strip()
        endereco = self.endereco_input.text().strip()
        
        if not cpf:
            QMessageBox.warning(self, "Aviso", "O CPF do cliente é obrigatório.")
            self.cpf_input.setFocus()
            return
            
        if not nome:
            QMessageBox.warning(self, "Aviso", "O nome do cliente é obrigatório.")
            self.nome_input.setFocus()
            return
        
        # Validação básica do CPF (somente números)
        if not cpf.isdigit() or len(cpf) != 11:
            QMessageBox.warning(self, "Aviso", "O CPF deve conter exatamente 11 dígitos numéricos.")
            self.cpf_input.setFocus()
            return
        
        cliente_id = self.id_input.text()
        
        try:
            if cliente_id:  # Atualização
                sucesso = ClienteController.atualizar_cliente(
                    int(cliente_id), cpf, nome, telefone, endereco
                )
                mensagem = "Cliente atualizado com sucesso!" if sucesso else "Erro ao atualizar cliente."
            else:  # Novo cadastro
                cliente = ClienteController.cadastrar_cliente(cpf, nome, telefone, endereco)
                sucesso = cliente is not None
                mensagem = "Cliente cadastrado com sucesso!" if sucesso else "Erro ao cadastrar cliente."
            
            if sucesso:
                self.limpar_campos()
                self.carregar_clientes()
                QMessageBox.information(self, "Sucesso", mensagem)
            else:
                QMessageBox.critical(self, "Erro", mensagem)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                QMessageBox.critical(self, "Erro", "Este CPF já está cadastrado no sistema.")
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar cliente: {str(e)}")
    
    def excluir_cliente(self):
        """Exclui um cliente selecionado."""
        cliente_id = self.id_input.text()
        
        if not cliente_id:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")
            return
        
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            "Tem certeza que deseja excluir este cliente?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            sucesso = ClienteController.excluir_cliente(int(cliente_id))
            
            if sucesso:
                self.limpar_campos()
                self.carregar_clientes()
                QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir cliente.")
    
    def selecionar_cliente(self, item):
        """Seleciona um cliente da tabela para edição.
        
        Args:
            item (QTableWidgetItem): Item clicado na tabela.
        """
        row = item.row()
        
        cliente_id = self.tabela_clientes.item(row, 0).text()
        cpf = self.tabela_clientes.item(row, 1).text()
        nome = self.tabela_clientes.item(row, 2).text()
        telefone = self.tabela_clientes.item(row, 3).text()
        endereco = self.tabela_clientes.item(row, 4).text()
        
        self.id_input.setText(cliente_id)
        self.cpf_input.setText(cpf)
        self.nome_input.setText(nome)
        self.telefone_input.setText(telefone)
        self.endereco_input.setText(endereco)
    
    def buscar_cliente(self):
        """Busca clientes por CPF ou lista todos se CPF estiver vazio."""
        cpf_busca = self.busca_cpf_input.text().strip()
        
        self.tabela_clientes.setRowCount(0)
        
        if cpf_busca:
            # Busca por CPF específico
            if not cpf_busca.isdigit():
                QMessageBox.warning(self, "Aviso", "Digite apenas números para o CPF.")
                return
                
            cliente = ClienteController.buscar_cliente_por_cpf(cpf_busca)
            
            if cliente:
                row = self.tabela_clientes.rowCount()
                self.tabela_clientes.insertRow(row)
                
                self.tabela_clientes.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
                self.tabela_clientes.setItem(row, 1, QTableWidgetItem(cliente.cpf or ""))
                self.tabela_clientes.setItem(row, 2, QTableWidgetItem(cliente.nome))
                self.tabela_clientes.setItem(row, 3, QTableWidgetItem(cliente.telefone))
                self.tabela_clientes.setItem(row, 4, QTableWidgetItem(cliente.endereco))
            else:
                QMessageBox.information(self, "Resultado", "Nenhum cliente encontrado com este CPF.")
        else:
            # Lista todos os clientes
            self.carregar_clientes()