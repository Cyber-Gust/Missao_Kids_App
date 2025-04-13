import os
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLineEdit, 
                            QListWidget, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QDialog, QFormLayout,
                            QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from src.database.db_manager import DatabaseManager
import datetime
from src.utils.helpers import WindowStateManager  # Importar o gerenciador

class CheckinWindow(QMainWindow):
    def __init__(self):
        super(CheckinWindow, self).__init__()
        self.db = DatabaseManager()
        self.initUI()
        
    def initUI(self):
        # Configurar a janela
        self.setWindowTitle("Check-in - Ministério Kids")
        self.setMinimumSize(800, 600)
        self.setObjectName("checkinWindow")
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Check-in de Crianças")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            margin-bottom: 20px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        main_layout.addWidget(title_label)
        
        # Área de pesquisa estilizada
        search_widget = QWidget()
        search_widget.setStyleSheet("""
            background-color: #F9FCFA; 
            border: 1px solid #D5E8D4; 
            border-radius: 8px; 
            padding: 10px;
        """)
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 10, 10, 10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite o nome da criança...")
        # Conectar o evento textChanged para atualizar a lista em tempo real
        self.search_input.textChanged.connect(self.searchChildRealTime)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #D5E8D4;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                color: #333333;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #A8D5BA;
                background-color: #F0F9F5;
            }
        """)
        
        search_layout.addWidget(self.search_input)
        main_layout.addWidget(search_widget)
        
        # Lista de crianças encontradas
        results_label = QLabel("Resultados da Pesquisa:")
        results_label.setStyleSheet("""
            font-size: 16px; 
            margin-top: 10px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        main_layout.addWidget(results_label)
        
        self.children_list = QListWidget()
        self.children_list.setMaximumHeight(200)
        self.children_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #D5E8D4;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #FFE6CC;
                color: #333333;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        # Conectar o evento de clique duplo para fazer check-in rápido
        self.children_list.itemDoubleClicked.connect(self.onChildDoubleClicked)
        main_layout.addWidget(self.children_list)
        
        # Botões de ação em um container estilizado
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet("""
            background-color: #F5F5F5; 
            border-radius: 5px; 
            padding: 10px;
        """)
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(15)
        
        self.btn_checkin = QPushButton("Check-in")
        self.btn_checkin.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 120px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #97C4A9;
            }
            QPushButton:pressed {
                background-color: #86B398;
            }
        """)
        self.btn_checkin.clicked.connect(self.doCheckin)
        
        self.btn_checkout = QPushButton("Check-out")
        self.btn_checkout.setStyleSheet("""
            QPushButton {
                background-color: #F9D5E5;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 120px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F0C6D6;
            }
            QPushButton:pressed {
                background-color: #E1B7C7;
            }
        """)
        self.btn_checkout.clicked.connect(self.doCheckout)
        
        self.btn_add_visitor = QPushButton("Adicionar Visitante")
        self.btn_add_visitor.setStyleSheet("""
            QPushButton {
                background-color: #FFD8B1;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 160px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FFCCA0;
            }
            QPushButton:pressed {
                background-color: #FFBF8F;
            }
        """)
        self.btn_add_visitor.clicked.connect(self.addVisitor)
        
        buttons_layout.addWidget(self.btn_checkin)
        buttons_layout.addWidget(self.btn_checkout)
        buttons_layout.addWidget(self.btn_add_visitor)
        
        main_layout.addWidget(buttons_widget)
        
        # Lista de crianças em check-in
        checkin_container = QWidget()
        checkin_container.setStyleSheet("""
            background-color: #F9FCFA; 
            border: 1px solid #D5E8D4; 
            border-radius: 8px; 
            padding: 10px;
        """)
        checkin_container_layout = QVBoxLayout(checkin_container)
        
        checkin_label = QLabel("Crianças em Check-in:")
        checkin_label.setStyleSheet("""
            font-size: 18px; 
            margin-bottom: 10px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        checkin_container_layout.addWidget(checkin_label)
        
        self.checkin_list = QListWidget()
        self.checkin_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #D5E8D4;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #FFE6CC;
                color: #333333;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F5F5F5;
            }
        """)
        # Conectar o evento de clique duplo para fazer check-out rápido
        self.checkin_list.itemDoubleClicked.connect(self.onCheckinDoubleClicked)
        checkin_container_layout.addWidget(self.checkin_list)
        
        main_layout.addWidget(checkin_container)
        
        # Carregar crianças em check-in
        self.loadCheckinList()

        # Botão de voltar flutuante (estilizado para combinar com o tema)
        self.btn_voltar_float = QPushButton("Voltar", self)
        self.btn_voltar_float.setGeometry(20, 20, 100, 40)
        self.btn_voltar_float.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #333333;
                border: none;
                border-radius: 20px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #97C4A9;
            }
            QPushButton:pressed {
                background-color: #86B398;
            }
        """)
        self.btn_voltar_float.clicked.connect(self.voltarMainWindow)
        
        # Garantir que o botão fique visível
        self.btn_voltar_float.raise_()

    def voltarMainWindow(self):
        # Salvar o estado atual da janela
        from src.utils.helpers import WindowStateManager
        window_manager = WindowStateManager.get_instance()
        window_manager.save_state(self)
        
        from src.interface.main_window import MainWindow
        self.main_window = MainWindow()
        # Restaurar o estado da janela
        window_manager.restore_state(self.main_window)
        self.main_window.show()
        self.close()
    
    def searchChildRealTime(self):
        """Busca crianças em tempo real enquanto o usuário digita"""
        # Verificar se o arquivo existe
        print(f"Procurando arquivo em: {self.db.criancas_file}")
        print(f"O arquivo existe? {os.path.exists(self.db.criancas_file)}")
        if os.path.exists(self.db.criancas_file):
            print(f"Tamanho do arquivo: {os.path.getsize(self.db.criancas_file)} bytes")
        
        search_text = self.search_input.text()
        if search_text:  # Buscar com qualquer texto (mesmo com 1 caractere)
            children = self.db.search_children(search_text)
            print(f"Resultados encontrados: {len(children)}")
            self.children_list.clear()
            for child in children:
                self.children_list.addItem(f"{child['nome']} ({child['idade']} anos) - Sala: {self.getSalaByAge(child['idade'])}")
        else:
            # Se o campo estiver vazio, limpar a lista
            self.children_list.clear()
    
    def onChildDoubleClicked(self, item):
        """Faz check-in rápido quando o usuário dá duplo clique em uma criança"""
        # Extrair o nome da criança do texto completo
        child_name = item.text().split(" (")[0]
        
        # Verificar se a criança já está em check-in
        if self.db.is_child_checked_in(child_name):
            QMessageBox.information(self, "Info", f"{child_name} já está em check-in")
            return
        
        # Fazer check-in
        self.db.do_checkin(child_name)
        self.loadCheckinList()
        QMessageBox.information(self, "Sucesso", f"Check-in de {child_name} realizado com sucesso!")
    
    def onCheckinDoubleClicked(self, item):
        """Faz check-out rápido quando o usuário dá duplo clique em uma criança na lista de check-in"""
        # Extrair o nome da criança do texto completo
        child_name = item.text().split(" (")[0]
        
        # Perguntar se realmente deseja fazer check-out
        reply = QMessageBox.question(self, "Confirmar Check-out", 
                                    f"Deseja fazer check-out de {child_name}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Fazer check-out
            self.db.do_checkout(child_name)
            self.loadCheckinList()
            QMessageBox.information(self, "Sucesso", f"Check-out de {child_name} realizado com sucesso!")
    
    def getSalaByAge(self, age):
        age = int(age)
        if age <= 2:
            return "Berçário"
        elif age == 3:
            return "Infantil 1"
        elif age <= 5:
            return "Infantil 2"
        elif age <= 7:
            return "Infantil 3"
        elif age <= 10:
            return "Infantil 4"
        else:
            return "Juniores"
    
    def doCheckin(self):
        selected_items = self.children_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma criança para fazer check-in")
            return
        
        selected_child = selected_items[0].text()
        # Extrair o nome da criança do texto completo
        child_name = selected_child.split(" (")[0]
        
        # Verificar se a criança já está em check-in
        if self.db.is_child_checked_in(child_name):
            QMessageBox.information(self, "Info", f"{child_name} já está em check-in")
            return
        
        # Fazer check-in
        self.db.do_checkin(child_name)
        self.loadCheckinList()
        QMessageBox.information(self, "Sucesso", f"Check-in de {child_name} realizado com sucesso!")
    
    def doCheckout(self):
        selected_items = self.checkin_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma criança para fazer check-out")
            return
        
        selected_child = selected_items[0].text()
        # Extrair o nome da criança do texto completo
        child_name = selected_child.split(" (")[0]
        
        # Fazer check-out
        self.db.do_checkout(child_name)
        self.loadCheckinList()
        QMessageBox.information(self, "Sucesso", f"Check-out de {child_name} realizado com sucesso!")
    
    def addVisitor(self):
        dialog = VisitorDialog(self)
        if dialog.exec_():
            visitor_data = dialog.getVisitorData()
            self.db.add_visitor(visitor_data)
            self.db.do_checkin(visitor_data['nome'])
            self.loadCheckinList()
            QMessageBox.information(self, "Sucesso", f"Visitante {visitor_data['nome']} adicionado com sucesso!")
    
    def loadCheckinList(self):
        self.checkin_list.clear()
        checked_in_children = self.db.get_checked_in_children()
        for child in checked_in_children:
            self.checkin_list.addItem(f"{child['nome']} ({child['idade']} anos) - Sala: {child['sala']}")


class VisitorDialog(QDialog):
    def __init__(self, parent=None):
        super(VisitorDialog, self).__init__(parent)
        self.setWindowTitle("Adicionar Visitante")
        self.setMinimumWidth(400)
        self.initUI()
    
    def initUI(self):
        layout = QFormLayout(self)
        
        self.nome_input = QLineEdit()
        self.idade_input = QLineEdit()
        self.responsavel_input = QLineEdit()
        self.telefone_input = QLineEdit()
        
        self.sala_combo = QComboBox()
        self.sala_combo.addItems(["Berçário", "Infantil 1", "Infantil 2", "Infantil 3", "Infantil 4", "Juniores"])
        
        layout.addRow("Nome:", self.nome_input)
        layout.addRow("Idade:", self.idade_input)
        layout.addRow("Sala:", self.sala_combo)
        layout.addRow("Responsável:", self.responsavel_input)
        layout.addRow("Telefone:", self.telefone_input)
        
        buttons_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_add = QPushButton("Adicionar")
        self.btn_add.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_add)
        
        layout.addRow("", buttons_layout)
    
    def getVisitorData(self):
        # Data atual para o cadastro
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        
        return {
            'nome': self.nome_input.text(),
            'idade': self.idade_input.text(),
            'sala': self.sala_combo.currentText(),
            'responsavel': self.responsavel_input.text(),
            'telefone': self.telefone_input.text(),  # Garantir que o telefone seja incluído
            'visitante': True,
            'data_cadastro': current_date  # Adicionar data de cadastro
        }