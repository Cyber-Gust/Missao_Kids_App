import os
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, 
    QWidget, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from src.interface.checkin import CheckinWindow
from src.interface.cadastro import CadastroWindow
from src.interface.galeria import GaleriaWindow
from src.interface.relatorios import RelatoriosWindow
from src.utils.helpers import WindowStateManager  # Importar o gerenciador

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.window_manager = WindowStateManager.get_instance()

        self.setWindowTitle("Missão Kids App")
        self.setMinimumSize(800, 600)

        self.setupUI()
        self.setBackground()
        
    def atualizarFonteBotoes(self):
        largura = self.width()
        if largura <= 800:
            tamanho_fonte = 12
        elif largura >= 1400:
            tamanho_fonte = 22
        else:
            # Interpolação linear entre 18 e 32
            tamanho_fonte = int(18 + (largura - 800) * (32 - 18) / (1400 - 800))
        fonte = QFont("Arial", tamanho_fonte)
        fonte.setBold(True)

        for btn in [self.btn_checkin, self.btn_cadastro, self.btn_galeria, self.btn_relatorios]:
            btn.setFont(fonte)   
            
    def calcularEspacoSuperior(self):
        # Espaço entre 8px (mín) e 38px (~1 cm) conforme altura da janela
        altura = self.height()
        if altura <= 600:
            return 19
        elif altura >= 900:
            return 50
        else:
            return int(8 + (altura - 600) * (38 - 8) / (900 - 600))         

    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Espaçador dinâmico no topo
        self.espacoTopo = QSpacerItem(
            0,
            self.calcularEspacoSuperior(),
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )
        main_layout.addItem(self.espacoTopo)

        # Layout horizontal dos botões
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # Botão Check-in (maior, laranja, sublinhado)
        font_checkin = QFont("Arial", 24)
        font_checkin.setBold(True)
        font_checkin.setUnderline(True)

        checkin_stylesheet = """
            QPushButton {
                color: #2abf39;
                background: transparent;
                border: none;
                padding: 12px 30px;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #ff7d2e;
            }
            QPushButton:pressed {
                color: #c04a09;
            }
        """

        self.btn_checkin = QPushButton("Check-in")
        self.btn_checkin.setFont(font_checkin)
        self.btn_checkin.setStyleSheet(checkin_stylesheet)

        # Botões restantes (iguais entre si, pretos)
        font_botao = QFont("Arial", 20)
        font_botao.setBold(True)
        botao_stylesheet = """
            QPushButton {
                color: #000000;
                background: transparent;
                border: none;
                padding: 12px 30px;
            }
            QPushButton:hover {
                color: #a0a0a0;
            }
            QPushButton:pressed {
                color: #606060;
            }
        """
        self.btn_cadastro = QPushButton("Cadastro")
        self.btn_cadastro.setFont(font_botao)
        self.btn_cadastro.setStyleSheet(botao_stylesheet)

        self.btn_galeria = QPushButton("Galeria")
        self.btn_galeria.setFont(font_botao)
        self.btn_galeria.setStyleSheet(botao_stylesheet)

        self.btn_relatorios = QPushButton("Relatórios")
        self.btn_relatorios.setFont(font_botao)
        self.btn_relatorios.setStyleSheet(botao_stylesheet)

        # Espaçadores proporcionais à largura total (em stretches)
        top_layout.addStretch(3)  # 40% da largura

        top_layout.addWidget(self.btn_checkin)
        top_layout.addStretch(0)
        top_layout.addWidget(self.btn_cadastro)
        top_layout.addStretch(0)
        top_layout.addWidget(self.btn_galeria)
        top_layout.addStretch(0)
        top_layout.addWidget(self.btn_relatorios)

        top_layout.addStretch(1)  # 10% da largura ou ajuste aqui se desejar mais à direita

        main_layout.addWidget(top_widget)

        # Espaço expansível abaixo
        main_layout.addStretch(1)

        # Sinais dos botões
        self.btn_checkin.clicked.connect(self.openCheckin)
        self.btn_cadastro.clicked.connect(self.openCadastro)
        self.btn_galeria.clicked.connect(self.openGaleria)
        self.btn_relatorios.clicked.connect(self.openRelatorios)

        # Ajusta fonte ao iniciar
        self.atualizarFonteBotoes()

    def setBackground(self):
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
            os.makedirs(os.path.join(self.base_dir, 'assets', 'images'), exist_ok=True)
            print(f"Diretório de imagens criado em: {os.path.join(self.base_dir, 'assets', 'images')}")
            self.setStyleSheet("background-color: #f8f9fa;")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.atualizarFonteBotoes()

        # ATUALIZA O ESPAÇO SUPERIOR DINÂMICO
        if hasattr(self, "espacoTopo") and self.espacoTopo is not None:
            self.espacoTopo.changeSize(
                0,
                self.calcularEspacoSuperior(),
                QSizePolicy.Minimum,
                QSizePolicy.Fixed
            )
            # Força o layout a recalcular
            self.centralWidget().layout().invalidate()
            self.centralWidget().layout().update()

        # Redimensionar o background
        for child in self.children():
            if isinstance(child, QLabel) and not child.text():
                child.setGeometry(0, 0, self.width(), self.height())
                
    def openCheckin(self):
        self.window_manager.save_state(self)
        self.checkin_window = CheckinWindow()
        self.window_manager.restore_state(self.checkin_window)
        self.checkin_window.show()
        self.hide()
        
    def openCadastro(self):
        self.window_manager.save_state(self)
        self.cadastro_window = CadastroWindow()
        self.window_manager.restore_state(self.cadastro_window)
        self.cadastro_window.show()
        self.hide()
        
    def openGaleria(self):
        self.window_manager.save_state(self)
        self.galeria_window = GaleriaWindow()
        self.window_manager.restore_state(self.galeria_window)
        self.galeria_window.show()
        self.hide()
        
    def openRelatorios(self):
        self.window_manager.save_state(self)
        self.relatorios_window = RelatoriosWindow()
        self.window_manager.restore_state(self.relatorios_window)
        self.relatorios_window.show()
        self.hide()