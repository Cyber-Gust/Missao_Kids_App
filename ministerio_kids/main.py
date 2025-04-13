import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from src.interface.main_window import MainWindow

def main():
    # Configurar o ambiente
    # Obter o diretório onde o script está localizado
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Definir o caminho para o diretório de dados
    DATA_DIR = os.path.join(BASE_DIR, "data")
    # Criar o diretório se não existir
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Iniciar a aplicação
    app = QApplication(sys.argv)
    
    # Estilo embutido - removendo os estilos dos botões principais
    style = """/* Estilo geral da aplicação */
QMainWindow, QDialog {
    background-color: #f8f9fa;
    color: #212529;
}

/* Estilo dos botões genéricos */
QPushButton:not(#btn_checkin):not(#btn_cadastro):not(#btn_galeria):not(#btn_relatorios) {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 4px;
    color: #495057;
    padding: 8px 16px;
    font-size: 14px;
}

QPushButton:not(#btn_checkin):not(#btn_cadastro):not(#btn_galeria):not(#btn_relatorios):hover {
    background-color: #dee2e6;
}

QPushButton:not(#btn_checkin):not(#btn_cadastro):not(#btn_galeria):not(#btn_relatorios):pressed {
    background-color: #adb5bd;
}

/* Campos de texto */
QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
}

QLineEdit:focus {
    border: 1px solid #80bdff;
}

/* Listas */
QListWidget {
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: white;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background-color: #f8d7da;
    color: #721c24;
}

/* Labels */
QLabel {
    color: #495057;
}

/* ComboBox */
QComboBox {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #ced4da;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background-color: #f8f9fa;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #adb5bd;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6c757d;
}"""
    
    app.setStyleSheet(style)
    
    # Criar e mostrar a janela principal
    window = MainWindow()
    window.show()
    
    # Executar o loop da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()