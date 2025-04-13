import os
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QHBoxLayout, QWidget, QFileDialog, QListWidget, 
                            QListWidgetItem, QMessageBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

class GaleriaWindow(QMainWindow):
    def __init__(self):
        super(GaleriaWindow, self).__init__()
        self.image_folder = "data/images"
        self.initUI()
        
    def initUI(self):
        # Configurar a janela
        self.setWindowTitle("Galeria - Ministério Kids")
        self.setMinimumSize(900, 600)
        self.setObjectName("galeriaWindow")
        
        # Criar pasta de imagens se não existir
        os.makedirs(self.image_folder, exist_ok=True)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Galeria de Fotos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            margin-bottom: 20px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        main_layout.addWidget(title_label)
        
        # Botões de ação em um container estilizado
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet("""
            background-color: #F9FCFA; 
            border: 1px solid #D5E8D4; 
            border-radius: 8px; 
            padding: 10px;
        """)
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(15)
        
        self.btn_add = QPushButton("Adicionar Imagens")
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
                min-width: 150px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #97C4A9;
            }
            QPushButton:pressed {
                background-color: #86B398;
            }
        """)
        
        # Tentar carregar o ícone se existir
        icon_path = "assets/icons/add.png"
        if os.path.exists(icon_path):
            self.btn_add.setIcon(QIcon(icon_path))
            self.btn_add.setIconSize(QSize(16, 16))
        
        self.btn_add.clicked.connect(self.addImages)
        
        self.btn_delete = QPushButton("Excluir Selecionadas")
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #F9D5E5;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
                min-width: 150px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F0C6D6;
            }
            QPushButton:pressed {
                background-color: #E1B7C7;
            }
        """)
        
        # Tentar carregar o ícone se existir
        icon_path = "assets/icons/delete.png"
        if os.path.exists(icon_path):
            self.btn_delete.setIcon(QIcon(icon_path))
            self.btn_delete.setIconSize(QSize(16, 16))
        
        self.btn_delete.clicked.connect(self.deleteImages)
        
        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addStretch(1)  # Adiciona espaço flexível à direita
        
        main_layout.addWidget(buttons_widget)
        
        # Área de visualização de imagens com scroll
        scroll_container = QWidget()
        scroll_container.setStyleSheet("""
            background-color: #F9FCFA; 
            border: 1px solid #D5E8D4; 
            border-radius: 8px; 
            padding: 5px;
        """)
        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(10, 10, 10, 10)
        
        gallery_label = QLabel("Fotos Missão Kids")
        gallery_label.setAlignment(Qt.AlignCenter)
        gallery_label.setStyleSheet("""
            font-size: 16px; 
            margin-bottom: 10px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        scroll_container_layout.addWidget(gallery_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #D5E8D4;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A8D5BA;
            }
        """)
        
        self.image_grid_widget = QWidget()
        self.image_grid_widget.setStyleSheet("background-color: white; border-radius: 5px;")
        self.image_grid = QGridLayout(self.image_grid_widget)
        self.image_grid.setContentsMargins(10, 10, 10, 10)
        self.image_grid.setSpacing(10)
        
        scroll_area.setWidget(self.image_grid_widget)
        scroll_container_layout.addWidget(scroll_area)
        
        main_layout.addWidget(scroll_container)
        
        # Carregar imagens existentes
        self.loadImages()

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
    
    def addImages(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Imagens (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            
            for file_path in selected_files:
                file_name = os.path.basename(file_path)
                destination = os.path.join(self.image_folder, file_name)
                
                # Verificar se o arquivo já existe
                if os.path.exists(destination):
                    reply = QMessageBox.question(self, "Arquivo Existente", 
                                                f"O arquivo {file_name} já existe. Deseja substituí-lo?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    
                    if reply == QMessageBox.No:
                        continue
                
                # Copiar o arquivo
                try:
                    with open(file_path, 'rb') as src_file:
                        with open(destination, 'wb') as dst_file:
                            dst_file.write(src_file.read())
                    
                    QMessageBox.information(self, "Sucesso", f"Imagem {file_name} adicionada com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao adicionar imagem: {e}")
            
            # Recarregar imagens
            self.loadImages()
    
    def loadImages(self):
        # Limpar grid existente
        for i in reversed(range(self.image_grid.count())):
            self.image_grid.itemAt(i).widget().setParent(None)
        
        # Verificar se a pasta existe
        if not os.path.exists(self.image_folder):
            return
        
        # Listar arquivos de imagem
        image_files = [f for f in os.listdir(self.image_folder) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        # Adicionar imagens ao grid
        row, col = 0, 0
        max_cols = 4  # Número de colunas no grid
        
        for image_file in image_files:
            image_path = os.path.join(self.image_folder, image_file)
            
            # Criar widget de imagem
            image_widget = ImageWidget(image_path, image_file)
            
            # Adicionar ao grid
            self.image_grid.addWidget(image_widget, row, col)
            
            # Atualizar posição
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def deleteImages(self):
        # Coletar imagens selecionadas
        selected_images = []
        
        for i in range(self.image_grid.count()):
            widget = self.image_grid.itemAt(i).widget()
            if isinstance(widget, ImageWidget) and widget.isSelected():
                selected_images.append(widget.image_path)
        
        if not selected_images:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem selecionada")
            return
        
        # Confirmar exclusão
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                    f"Tem certeza que deseja excluir {len(selected_images)} imagem(ns)?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Excluir imagens
            for image_path in selected_images:
                try:
                    os.remove(image_path)
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir imagem: {e}")
            
            # Recarregar imagens
            self.loadImages()
            QMessageBox.information(self, "Sucesso", "Imagens excluídas com sucesso!")

class ImageWidget(QWidget):
    def __init__(self, image_path, image_name):
        super(ImageWidget, self).__init__()
        self.image_path = image_path
        self.image_name = image_name
        self.selected = False
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Imagem
        self.image_label = QLabel()
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Nome da imagem
        name_label = QLabel(self.image_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setMaximumWidth(200)
        
        # Adicionar ao layout
        layout.addWidget(self.image_label)
        layout.addWidget(name_label)
        
        # Estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)
        
        # Tamanho fixo
        self.setFixedSize(220, 200)
    
    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.updateStyle()
    
    def updateStyle(self):
        if self.selected:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f8d7da;
                    border: 2px solid #721c24;
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                }
            """)
    
    def isSelected(self):
        return self.selected