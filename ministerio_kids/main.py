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
    
    
    
    # Criar e mostrar a janela principal
    window = MainWindow()
    window.show()
    
    # Executar o loop da aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()