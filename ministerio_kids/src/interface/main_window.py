import os
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QWidget, QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

from src.interface.checkin import CheckinWindow
from src.interface.cadastro import CadastroWindow
from src.interface.galeria import GaleriaWindow
from src.interface.relatorios import RelatoriosWindow
from src.utils.helpers import WindowStateManager  # Importar o gerenciador

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Obter o caminho absoluto para o diretório do projeto
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Inicializar o gerenciador de estado da janela
        self.window_manager = WindowStateManager.get_instance()
        
        # Configurar a janela
        self.setWindowTitle("Ministério Kids")
        self.setMinimumSize(800, 600)
        
        # Criar a interface completa
        self.setupUI()
        
        # Configurar o background
        self.setBackground()
    
    def setupUI(self):
        """Cria toda a interface da janela principal"""
        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Criar layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Criar widget para os botões no topo
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setAlignment(Qt.AlignCenter)
        top_layout.setContentsMargins(0, 20, 0, 20)
        
        # Adicionar espaçadores flexíveis antes e depois dos botões
        top_layout.addStretch(1)  # Espaçador flexível à esquerda
        
        # Criar os botões estilizados
        # Primeiro botão - Check-in (Arial 16, negrito, sublinhado, cor #f05e0b)
        self.btn_checkin = QPushButton("Check-in")
        self.btn_checkin.setObjectName("btn_checkin")
        font_checkin = QFont("Arial", 16)
        font_checkin.setBold(True)
        font_checkin.setUnderline(True)
        self.btn_checkin.setFont(font_checkin)
        self.btn_checkin.setStyleSheet("""
            QPushButton {
                color: #f05e0b;
                background: transparent;
                border: none;
                padding: 10px 20px;
            }
            QPushButton:hover {
                color: #ff7d2e;
            }
            QPushButton:pressed {
                color: #c04a09;
            }
        """)
        
        # Outros botões - Arial 14, negrito, cor #808080 (cinza)
        self.btn_cadastro = QPushButton("Cadastro")
        self.btn_cadastro.setObjectName("btn_cadastro")
        
        self.btn_galeria = QPushButton("Galeria")
        self.btn_galeria.setObjectName("btn_galeria")
        
        self.btn_relatorios = QPushButton("Relatórios")
        self.btn_relatorios.setObjectName("btn_relatorios")
        
        other_buttons = [self.btn_cadastro, self.btn_galeria, self.btn_relatorios]
        
        for btn in other_buttons:
            font_other = QFont("Arial", 14)
            font_other.setBold(True)
            btn.setFont(font_other)
            btn.setStyleSheet("""
                QPushButton {
                    color: #808080;
                    background: transparent;
                    border: none;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    color: #a0a0a0;
                }
                QPushButton:pressed {
                    color: #606060;
                }
            """)
        
        # Adicionar os botões ao layout
        top_layout.addWidget(self.btn_checkin)
        top_layout.addWidget(self.btn_cadastro)
        top_layout.addWidget(self.btn_galeria)
        top_layout.addWidget(self.btn_relatorios)
        
        # Adicionar espaçador flexível à direita
        top_layout.addStretch(1)
        
        # Configurar o espaçamento entre os botões
        top_layout.setSpacing(30)
        
        # Adicionar o widget de botões ao layout principal
        main_layout.addWidget(top_widget)
        
        # Adicionar um espaço em branco para o conteúdo principal
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(content_widget, 1)  # 1 é o stretch factor
        
        # Conectar sinais
        self.btn_checkin.clicked.connect(self.openCheckin)
        self.btn_cadastro.clicked.connect(self.openCadastro)
        self.btn_galeria.clicked.connect(self.openGaleria)
        self.btn_relatorios.clicked.connect(self.openRelatorios)
    
    def setBackground(self):
        # Configurar o background com caminho absoluto
        background_path = os.path.join(self.base_dir, 'assets', 'images', 'background.jpg')
        if os.path.exists(background_path):
            pixmap = QPixmap(background_path)
            background_label = QLabel(self)
            background_label.setPixmap(pixmap)
            background_label.setScaledContents(True)
            background_label.setGeometry(0, 0, self.width(), self.height())
            background_label.lower()
        else:
            print(f"Imagem de fundo não encontrada: {background_path}")
            # Criar diretório de imagens se não existir
            os.makedirs(os.path.join(self.base_dir, 'assets', 'images'), exist_ok=True)
            print(f"Diretório de imagens criado em: {os.path.join(self.base_dir, 'assets', 'images')}")
            
            # Definir um background alternativo (cor sólida)
            self.setStyleSheet("background-color: #f8f9fa;")
    
    def resizeEvent(self, event):
        """Redimensiona o background e ajusta o espaçamento dos botões quando a janela é redimensionada"""
        super().resizeEvent(event)
        
        # Ajustar o espaçamento dos botões com base na largura da janela
        window_width = self.width()
        # Calcular o espaçamento proporcional (aumenta com a largura da janela)
        spacing = int(window_width * 0.04)  # 4% da largura da janela
        
        # Encontrar o layout dos botões e ajustar o espaçamento
        for child in self.centralWidget().children():
            if isinstance(child, QWidget):
                for grandchild in child.children():
                    if isinstance(grandchild, QHBoxLayout):
                        grandchild.setSpacing(spacing)
        
        # Redimensionar o background
        for child in self.children():
            if isinstance(child, QLabel) and not child.text():
                # Assumimos que é o label de background (sem texto)
                child.setGeometry(0, 0, self.width(), self.height())
    
    def openCheckin(self):
        # Salvar o estado atual da janela
        self.window_manager.save_state(self)
        
        self.checkin_window = CheckinWindow()
        # Restaurar o estado da janela
        self.window_manager.restore_state(self.checkin_window)
        self.checkin_window.show()
        self.hide()
    
    def openCadastro(self):
        # Salvar o estado atual da janela
        self.window_manager.save_state(self)
        
        self.cadastro_window = CadastroWindow()
        # Restaurar o estado da janela
        self.window_manager.restore_state(self.cadastro_window)
        self.cadastro_window.show()
        self.hide()
    
    def openGaleria(self):
        # Salvar o estado atual da janela
        self.window_manager.save_state(self)
        
        self.galeria_window = GaleriaWindow()
        # Restaurar o estado da janela
        self.window_manager.restore_state(self.galeria_window)
        self.galeria_window.show()
        self.hide()
    
    def openRelatorios(self):
        # Salvar o estado atual da janela
        self.window_manager.save_state(self)
        
        self.relatorios_window = RelatoriosWindow()
        # Restaurar o estado da janela
        self.window_manager.restore_state(self.relatorios_window)
        self.relatorios_window.show()
        self.hide()