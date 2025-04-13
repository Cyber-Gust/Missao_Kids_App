# src/interface/base_window.py
import os
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import Qt

class BaseSecondaryWindow(QMainWindow):
    """Classe base para todas as janelas secundárias"""
    
    def __init__(self):
        super(BaseSecondaryWindow, self).__init__()
        
        # Obter o caminho absoluto para o diretório do projeto
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Adicionar botão de voltar
        self.addBackButton()
    
    def addBackButton(self):
        """Adiciona um botão de voltar no canto superior esquerdo"""
        # Criar o botão
        back_button = QPushButton("←")  # Seta para esquerda
        back_button.setObjectName("btn_back")
        
        # Estilizar o botão como uma seta sem borda
        back_button.setStyleSheet("""
            QPushButton#btn_back {
                background-color: transparent;
                border: none;
                color: #721c24;
                font-size: 24px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton#btn_back:hover {
                color: #f5c6cb;
            }
        """)
        
        # Definir tamanho fixo
        back_button.setFixedSize(40, 40)
        
        # Posicionar o botão no canto superior esquerdo
        back_button.setParent(self)
        back_button.move(10, 10)
        
        # Conectar o sinal
        back_button.clicked.connect(self.goBack)
    
    def goBack(self):
        """Volta para a janela principal"""
        # Importação local para evitar importação circular
        from src.interface.main_window import MainWindow
        
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()