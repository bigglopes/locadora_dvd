import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from PyQt5.QtCore import Qt

from views.cliente_view import ClienteView
from views.dvd_view import DVDView
from views.aluguel_view import AluguelView
from views.dashboard_view import DashboardView
from database.config import DatabaseConfig

class MainWindow(QMainWindow):
    """Janela principal da aplicação."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sistema de Locadora de DVDs")
        self.setGeometry(100, 100, 1000, 600)
        
        # Inicializa o banco de dados
        DatabaseConfig.initialize_database()
        
        # Cria o widget de abas
        self.tab_widget = QTabWidget()
        
        # Cria as abas
        self.dashboard_view = DashboardView()
        self.cliente_view = ClienteView()
        self.dvd_view = DVDView()
        self.aluguel_view = AluguelView()
        
        # Adiciona as abas ao widget
        self.tab_widget.addTab(self.aluguel_view, "📋 Aluguéis")
        self.tab_widget.addTab(self.cliente_view, "👥 Clientes")
        self.tab_widget.addTab(self.dvd_view, "💿 DVDs")
        self.tab_widget.addTab(self.dashboard_view, "📊 Dashboard")
        
        
        
        # Define o widget central
        self.setCentralWidget(self.tab_widget)
        
        # Conecta os sinais
        self.tab_widget.currentChanged.connect(self.tab_changed)
    
    def tab_changed(self, index):
        """Manipula a mudança de aba.
        
        Args:
            index (int): Índice da aba selecionada.
        """
        # Atualiza dados conforme a aba selecionada
        if index == 3:  # Aba de Dashboard
            self.dashboard_view.carregar_dados()
        elif index == 0:  # Aba de Aluguéis
            self.aluguel_view.atualizar_combo_clientes()
            self.aluguel_view.atualizar_combo_dvds()

def main():
    """Função principal para iniciar a aplicação."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()