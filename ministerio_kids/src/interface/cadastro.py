from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLineEdit, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, 
                            QDateEdit, QComboBox, QCheckBox, QTextEdit, 
                            QListWidget, QMessageBox, QDialog, QGroupBox,
                            QRadioButton, QScrollArea)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QIcon
import os
import datetime
from src.database.db_manager import DatabaseManager

class CadastroWindow(QMainWindow):
    def __init__(self):
        super(CadastroWindow, self).__init__()
        self.db = DatabaseManager()
        self.initUI()
        
    def initUI(self):
        # Configurar a janela
        self.setWindowTitle("Cadastro - Ministério Kids")
        self.setMinimumSize(900, 700)
        self.setObjectName("cadastroWindow")  # Para estilização específica
        
        # Widget central com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        self.setCentralWidget(scroll_area)
        
        # Container para o conteúdo
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        scroll_area.setWidget(content_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Cadastro de Crianças")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            margin-bottom: 20px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        main_layout.addWidget(title_label)
        
        # Layout de duas colunas
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)
        
        # Coluna esquerda - Formulário
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        
        # Dados básicos
        basic_group = QGroupBox("Dados Básicos")
        basic_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        basic_layout = QFormLayout()
        basic_layout.setSpacing(10)
        basic_layout.setLabelAlignment(Qt.AlignRight)
        
        self.nome_input = QLineEdit()
        self.idade_input = QLineEdit()
        self.data_nascimento = QDateEdit()
        self.data_nascimento.setDisplayFormat("dd/MM/yyyy")
        self.data_nascimento.setDate(QDate.currentDate())
        self.data_nascimento.setCalendarPopup(True)
        
        # Estilizar campos de entrada
        input_style = """
            QLineEdit, QDateEdit, QComboBox, QTextEdit {
                border: 1px solid #D5E8D4;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #A8D5BA;
                background-color: #F0F9F5;
            }
        """
        
        self.nome_input.setStyleSheet(input_style)
        self.idade_input.setStyleSheet(input_style)
        self.data_nascimento.setStyleSheet(input_style)
        
        basic_layout.addRow("Nome da Criança:", self.nome_input)
        basic_layout.addRow("Idade:", self.idade_input)
        basic_layout.addRow("Data de Nascimento:", self.data_nascimento)
        
        basic_group.setLayout(basic_layout)
        form_layout.addWidget(basic_group)
        
        # Responsáveis
        resp_group = QGroupBox("Responsáveis")
        resp_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        resp_layout = QFormLayout()
        resp_layout.setSpacing(10)
        resp_layout.setLabelAlignment(Qt.AlignRight)
        
        self.pai_input = QLineEdit()
        self.mae_input = QLineEdit()
        self.outro_resp_input = QLineEdit()
        
        self.pai_input.setStyleSheet(input_style)
        self.mae_input.setStyleSheet(input_style)
        self.outro_resp_input.setStyleSheet(input_style)
        
        resp_layout.addRow("Pai:", self.pai_input)
        resp_layout.addRow("Mãe:", self.mae_input)
        resp_layout.addRow("Outro Responsável:", self.outro_resp_input)
        
        resp_group.setLayout(resp_layout)
        form_layout.addWidget(resp_group)
        
        # Endereço
        end_group = QGroupBox("Endereço")
        end_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        end_layout = QFormLayout()
        end_layout.setSpacing(10)
        end_layout.setLabelAlignment(Qt.AlignRight)
        
        self.endereco_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        
        self.endereco_input.setStyleSheet(input_style)
        self.bairro_input.setStyleSheet(input_style)
        self.cidade_input.setStyleSheet(input_style)
        
        end_layout.addRow("Endereço:", self.endereco_input)
        end_layout.addRow("Bairro:", self.bairro_input)
        end_layout.addRow("Cidade:", self.cidade_input)
        
        end_group.setLayout(end_layout)
        form_layout.addWidget(end_group)
        
        # Informações adicionais
        info_group = QGroupBox("Informações Adicionais")
        info_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        info_layout = QFormLayout()
        info_layout.setSpacing(10)
        info_layout.setLabelAlignment(Qt.AlignRight)
        
        self.membro_combo = QComboBox()
        self.membro_combo.addItems(["Sim", "Não"])
        
        self.batizado_combo = QComboBox()
        self.batizado_combo.addItems(["Sim", "Não"])
        
        self.doenca_layout = QHBoxLayout()
        self.doenca_combo = QComboBox()
        self.doenca_combo.addItems(["Não", "Sim"])
        self.doenca_combo.currentIndexChanged.connect(self.toggleDoencaInput)
        self.doenca_input = QLineEdit()
        self.doenca_input.setPlaceholderText("Especifique a doença...")
        self.doenca_input.setVisible(False)
        self.doenca_layout.addWidget(self.doenca_combo)
        self.doenca_layout.addWidget(self.doenca_input)
        
        self.alergia_layout = QHBoxLayout()
        self.alergia_combo = QComboBox()
        self.alergia_combo.addItems(["Não", "Sim"])
        self.alergia_combo.currentIndexChanged.connect(self.toggleAlergiaInput)
        self.alergia_input = QLineEdit()
        self.alergia_input.setPlaceholderText("Especifique a alergia...")
        self.alergia_input.setVisible(False)
        self.alergia_layout.addWidget(self.alergia_combo)
        self.alergia_layout.addWidget(self.alergia_input)
        
        # Estilizar combos e inputs
        self.membro_combo.setStyleSheet(input_style)
        self.batizado_combo.setStyleSheet(input_style)
        self.doenca_combo.setStyleSheet(input_style)
        self.doenca_input.setStyleSheet(input_style)
        self.alergia_combo.setStyleSheet(input_style)
        self.alergia_input.setStyleSheet(input_style)
        
        info_layout.addRow("É membro da Missão Atos?", self.membro_combo)
        info_layout.addRow("Já passou pelo batismo de arrependimento?", self.batizado_combo)
        info_layout.addRow("Apresenta doença crônica?", self.doenca_layout)
        info_layout.addRow("Apresenta alguma alergia?", self.alergia_layout)
        
        info_group.setLayout(info_layout)
        form_layout.addWidget(info_group)
        
        # Contato e permissões
        contato_group = QGroupBox("Contato e Permissões")
        contato_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        contato_layout = QFormLayout()
        contato_layout.setSpacing(10)
        contato_layout.setLabelAlignment(Qt.AlignRight)

        self.telefone_input = QLineEdit()
        self.telefone_input.setStyleSheet(input_style)
        self.telefone_input.setPlaceholderText("(00) 00000-0000")
        contato_layout.addRow("Telefone:", self.telefone_input)

        self.conversa_combo = QComboBox()
        self.conversa_combo.addItems(["Não", "Sim, presencial", "Sim, online"])

        self.visita_combo = QComboBox()
        self.visita_combo.addItems(["Não", "Sim"])

        self.fotos_combo = QComboBox()
        self.fotos_combo.addItems(["Não", "Sim"])

        self.conversa_combo.setStyleSheet(input_style)
        self.visita_combo.setStyleSheet(input_style)
        self.fotos_combo.setStyleSheet(input_style)

        contato_layout.addRow("Gostaria de conversar com monitora do Missão Kids?", self.conversa_combo)
        contato_layout.addRow("Aceita receber visita de monitor para oração?", self.visita_combo)
        contato_layout.addRow("Permite postagens de fotos em redes sociais?", self.fotos_combo)

        contato_group.setLayout(contato_layout)
        form_layout.addWidget(contato_group)
        
        # Observações
        obs_group = QGroupBox("Observações")
        obs_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #D5E8D4;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: #F9FCFA;
                font-weight: bold;
                color: #5D9B7C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: white;
            }
        """)
        obs_layout = QVBoxLayout()
        
        self.obs_input = QTextEdit()
        self.obs_input.setMaximumHeight(100)
        self.obs_input.setStyleSheet(input_style)
        
        obs_layout.addWidget(self.obs_input)
        
        obs_group.setLayout(obs_layout)
        form_layout.addWidget(obs_group)
        
        # Concordância
        self.concordo_check = QCheckBox("Concordo com as informações contidas nesse formulário")
        self.concordo_check.setStyleSheet("""
            QCheckBox {
                color: #333333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #D5E8D4;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #A8D5BA;
                background-color: #A8D5BA;
            }
        """)
        form_layout.addWidget(self.concordo_check)
        
        # Botões de ação
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet("background-color: #F5F5F5; border-radius: 5px; padding: 10px;")
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(15)
        
        self.btn_limpar = QPushButton("Limpar")
        self.btn_limpar.setObjectName("btn_limpar")
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background-color: #D4E5F7;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #C3D4E6;
            }
        """)
        self.btn_limpar.clicked.connect(self.limparFormulario)
        
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setObjectName("btn_cadastrar")
        self.btn_cadastrar.setStyleSheet("""
            QPushButton {
                background-color: #FFD8B1;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #FFCCA0;
            }
        """)
        self.btn_cadastrar.clicked.connect(self.cadastrarCrianca)
        
        buttons_layout.addWidget(self.btn_limpar)
        buttons_layout.addWidget(self.btn_cadastrar)
        
        form_layout.addWidget(buttons_widget)
        
        # Coluna direita - Lista de crianças cadastradas
        list_layout = QVBoxLayout()
        list_layout.setSpacing(10)
        
        list_label = QLabel("Crianças Cadastradas")
        list_label.setAlignment(Qt.AlignCenter)
        list_label.setStyleSheet("""
            font-size: 18px; 
            margin-bottom: 10px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        
        self.children_list = QListWidget()
        self.children_list.setMinimumWidth(300)
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
        
        list_buttons_widget = QWidget()
        list_buttons_widget.setStyleSheet("background-color: #F5F5F5; border-radius: 5px; padding: 8px;")
        list_buttons = QHBoxLayout(list_buttons_widget)
        list_buttons.setContentsMargins(8, 8, 8, 8)
        list_buttons.setSpacing(10)
        
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #A8D5BA;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #97C4A9;
            }
        """)
        self.btn_editar.clicked.connect(self.editarCrianca)
        
        self.btn_excluir = QPushButton("Excluir")
        self.btn_excluir.setObjectName("btn_excluir")
        self.btn_excluir.setStyleSheet("""
            QPushButton {
                background-color: #F9D5E5;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0C6D6;
            }
        """)
        self.btn_excluir.clicked.connect(self.excluirCrianca)
        
        list_buttons.addWidget(self.btn_editar)
        list_buttons.addWidget(self.btn_excluir)
        
        list_layout.addWidget(list_label)
        list_layout.addWidget(self.children_list)
        list_layout.addWidget(list_buttons_widget)
        
        # Adicionar as colunas ao layout principal
        columns_layout.addLayout(form_layout, 2)
        columns_layout.addLayout(list_layout, 1)
        
        main_layout.addLayout(columns_layout)
        
        # Carregar a lista de crianças
        self.carregarListaCriancas()

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
    
    def toggleDoencaInput(self, index):
        self.doenca_input.setVisible(index == 1)  # Mostrar se "Sim" estiver selecionado
    
    def toggleAlergiaInput(self, index):
        self.alergia_input.setVisible(index == 1)  # Mostrar se "Sim" estiver selecionado
    
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
    
    def limparFormulario(self):
        self.nome_input.clear()
        self.idade_input.clear()
        self.data_nascimento.setDate(QDate.currentDate())
        self.pai_input.clear()
        self.mae_input.clear()
        self.outro_resp_input.clear()
        self.endereco_input.clear()
        self.bairro_input.clear()
        self.cidade_input.clear()
        self.telefone_input.clear()  # Limpar campo de telefone
        self.doenca_combo.setCurrentIndex(0)
        self.doenca_input.clear()
        self.doenca_input.setVisible(False)
        self.alergia_combo.setCurrentIndex(0)
        self.alergia_input.clear()
        self.alergia_input.setVisible(False)
        self.conversa_combo.setCurrentIndex(0)
        self.visita_combo.setCurrentIndex(0)
        self.fotos_combo.setCurrentIndex(0)
        self.obs_input.clear()
        self.concordo_check.setChecked(False)
    
    def cadastrarCrianca(self):
        # Verificar se o formulário está preenchido corretamente
        if not self.nome_input.text():
            QMessageBox.warning(self, "Aviso", "O nome da criança é obrigatório")
            return
        
        if not self.idade_input.text():
            QMessageBox.warning(self, "Aviso", "A idade da criança é obrigatória")
            return
        
        if not self.concordo_check.isChecked():
            QMessageBox.warning(self, "Aviso", "É necessário concordar com as informações do formulário")
            return
        
        # Coletar dados do formulário
        child_data = {
            'nome': self.nome_input.text(),
            'idade': self.idade_input.text(),
            'data_nascimento': self.data_nascimento.date().toString("dd/MM/yyyy"),
            'pai': self.pai_input.text(),
            'mae': self.mae_input.text(),
            'outro_responsavel': self.outro_resp_input.text(),
            'endereco': self.endereco_input.text(),
            'bairro': self.bairro_input.text(),
            'cidade': self.cidade_input.text(),
            'telefone': self.telefone_input.text(),
            'membro': self.membro_combo.currentText(),
            'batizado': self.batizado_combo.currentText(),
            'doenca_cronica': self.doenca_input.text() if self.doenca_combo.currentIndex() == 1 else "Não",
            'alergia': self.alergia_input.text() if self.alergia_combo.currentIndex() == 1 else "Não",
            'conversa_monitor': self.conversa_combo.currentText(),
            'visita': self.visita_combo.currentText(),
            'permite_fotos': self.fotos_combo.currentText(),
            'observacoes': self.obs_input.toPlainText(),
            'visitante': 'Não',
            'data_cadastro': QDate.currentDate().toString("dd/MM/yyyy")
        }
        
        try:
            import csv
            import os
            
            # Determinar o caminho absoluto do arquivo
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            criancas_file = os.path.join(base_dir, 'data', 'criancas.csv')
            
            print(f"Salvando criança no arquivo: {criancas_file}")
            
            # Verificar se o diretório existe
            os.makedirs(os.path.dirname(criancas_file), exist_ok=True)
            
            # Verificar se o arquivo existe e tem conteúdo
            file_exists = os.path.exists(criancas_file) and os.path.getsize(criancas_file) > 0
            
            # Definir os campos padrão na ordem correta
            default_fields = [
                'nome', 'idade', 'data_nascimento', 'pai', 'mae', 'outro_responsavel', 
                'endereco', 'bairro', 'cidade', 'telefone', 'membro', 'batizado', 'doenca_cronica',
                'alergia', 'conversa_monitor', 'visita', 'permite_fotos', 'observacoes',
                'visitante', 'data_cadastro'
            ]
            
            # Abrir o arquivo no modo apropriado
            with open(criancas_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=default_fields)
                
                # Escrever o cabeçalho se o arquivo não existir ou estiver vazio
                if not file_exists:
                    writer.writeheader()
                    print("Escrevendo cabeçalho no arquivo")
                
                # Escrever a linha de dados
                writer.writerow(child_data)
                print(f"Criança {child_data['nome']} adicionada ao arquivo")
            
            # Verificar se o arquivo foi atualizado
            if os.path.exists(criancas_file):
                file_size = os.path.getsize(criancas_file)
                print(f"Tamanho do arquivo após salvamento: {file_size} bytes")
                
                # Ler o conteúdo do arquivo para verificar
                with open(criancas_file, 'r', encoding='utf-8') as f:
                    content = f.read(200)  # Ler apenas os primeiros 200 caracteres
                    print(f"Primeiros caracteres do arquivo: {content}")
            
            QMessageBox.information(self, "Sucesso", f"Criança {child_data['nome']} cadastrada com sucesso!")
            self.limparFormulario()
            self.carregarListaCriancas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar criança: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def carregarListaCriancas(self):
        # Limpar a lista atual
        self.children_list.clear()
        
        try:
            import os
            import csv
            
            # Determinar o caminho absoluto do arquivo
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            criancas_file = os.path.join(base_dir, 'data', 'criancas.csv')
            
            print(f"Carregando crianças do arquivo: {criancas_file}")
            
            # Verificar se o arquivo existe
            if not os.path.exists(criancas_file):
                print(f"Arquivo {criancas_file} não encontrado")
                return
            
            # Ler diretamente do arquivo
            with open(criancas_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                children = list(reader)
                
                print(f"Lidas {len(children)} crianças do arquivo")
                
                # Adicionar crianças à lista
                for child in children:
                    nome = child.get('nome', '')
                    idade = child.get('idade', '')
                    item_text = f"{nome} ({idade} anos)"
                    self.children_list.addItem(item_text)
        except Exception as e:
            print(f"Erro ao carregar lista de crianças: {e}")
            import traceback
            traceback.print_exc()

    def editarCrianca(self):
        selected_items = self.children_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma criança para editar")
            return
        
        selected_items = self.children_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma criança para excluir")
            return

        selected_child = selected_items[0].text()
        # Extrair o nome da criança do texto completo
        child_name = selected_child.split(" (")[0]
        
        # Buscar dados da criança
        child_data = self.db.get_child_by_name(child_name)
        if not child_data:
            QMessageBox.warning(self, "Aviso", f"Não foi possível encontrar os dados de {child_name}")
            return
        
        # Abrir diálogo de edição
        dialog = EditChildDialog(child_data, self)
        if dialog.exec_():
            updated_data = dialog.getChildData()
            if self.db.update_child(child_name, updated_data):
                QMessageBox.information(self, "Sucesso", f"Dados de {updated_data['nome']} atualizados com sucesso!")
                self.carregarListaCriancas()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao atualizar dados. Tente novamente.")
    
    def excluirCrianca(self):
        selected_items = self.children_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione uma criança para excluir")
            return
        
        selected_child = selected_items[0].text()
        # Extrair o nome da criança do texto completo
        child_name = selected_child.split(" (")[0].strip()
        
        print(f"Tentando excluir criança: '{child_name}'")
        
        # Confirmar exclusão
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                f"Tem certeza que deseja excluir {child_name}?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                import csv
                import os
                
                # Determinar o caminho absoluto do arquivo
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                criancas_file = os.path.join(base_dir, 'data', 'criancas.csv')
                
                print(f"Excluindo criança do arquivo: {criancas_file}")
                
                # Verificar se o arquivo existe
                if not os.path.exists(criancas_file):
                    QMessageBox.critical(self, "Erro", f"Arquivo não encontrado: {criancas_file}")
                    return
                
                # Ler diretamente do arquivo
                children = []
                updated_children = []
                found = False
                
                with open(criancas_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    fieldnames = reader.fieldnames
                    
                    # Imprimir cabeçalhos para depuração
                    print(f"Cabeçalhos do CSV: {fieldnames}")
                    
                    for row in reader:
                        # Imprimir cada linha para depuração
                        print(f"Linha do CSV: {row}")
                        
                        children.append(row)
                        nome_csv = row.get('nome', '').strip()
                        
                        print(f"Comparando '{nome_csv}' com '{child_name}'")
                        
                        # Comparação case-insensitive
                        if nome_csv.lower() != child_name.lower():
                            updated_children.append(row)
                        else:
                            found = True
                            print(f"Criança encontrada: {nome_csv}")
                
                if not found:
                    # Tentar uma abordagem mais flexível
                    print("Criança não encontrada, tentando busca flexível...")
                    updated_children = []
                    found = False
                    
                    for child in children:
                        nome_csv = child.get('nome', '').strip()
                        
                        # Verificar se o nome da criança está contido no nome do CSV ou vice-versa
                        if child_name.lower() in nome_csv.lower() or nome_csv.lower() in child_name.lower():
                            found = True
                            print(f"Correspondência parcial encontrada: '{nome_csv}'")
                        else:
                            updated_children.append(child)
                
                if not found:
                    QMessageBox.warning(self, "Aviso", f"Não foi possível encontrar {child_name}")
                    return
                
                print(f"Lidas {len(children)} crianças, {len(updated_children)} após exclusão")
                
                # Escrever a lista atualizada de volta ao arquivo
                with open(criancas_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_children)
                    print(f"Arquivo salvo com {len(updated_children)} crianças")
                
                # Atualizar a interface
                QMessageBox.information(self, "Sucesso", f"{child_name} excluído com sucesso!")
                
                # Forçar atualização da lista
                self.children_list.clear()
                self.carregarListaCriancas()
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir criança: {str(e)}")
                import traceback
                traceback.print_exc()

class EditChildDialog(QDialog):
    def __init__(self, child_data, parent=None):
        super(EditChildDialog, self).__init__(parent)
        self.child_data = child_data
        self.setWindowTitle(f"Editar - {child_data['nome']}")
        self.setMinimumWidth(500)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        self.nome_input = QLineEdit(self.child_data['nome'])
        self.idade_input = QLineEdit(self.child_data['idade'])
        
        self.data_nascimento = QDateEdit()
        self.data_nascimento.setDisplayFormat("dd/MM/yyyy")
        if self.child_data['data_nascimento']:
            self.data_nascimento.setDate(QDate.fromString(self.child_data['data_nascimento'], "dd/MM/yyyy"))
        else:
            self.data_nascimento.setDate(QDate.currentDate())
        self.data_nascimento.setCalendarPopup(True)
        
        self.pai_input = QLineEdit(self.child_data['pai'])
        self.mae_input = QLineEdit(self.child_data['mae'])
        self.outro_resp_input = QLineEdit(self.child_data['outro_responsavel'])
        
        self.endereco_input = QLineEdit(self.child_data['endereco'])
        self.bairro_input = QLineEdit(self.child_data['bairro'])
        self.cidade_input = QLineEdit(self.child_data['cidade'])
        
        # Adicionar campo de telefone
        self.telefone_input = QLineEdit(self.child_data.get('telefone', ''))
        
        self.membro_combo = QComboBox()
        self.membro_combo.addItems(["Sim", "Não"])
        self.membro_combo.setCurrentText(self.child_data['membro'])
        
        self.batizado_combo = QComboBox()
        self.batizado_combo.addItems(["Sim", "Não"])
        self.batizado_combo.setCurrentText(self.child_data['batizado'])
        
        self.doenca_combo = QComboBox()
        self.doenca_combo.addItems(["Não", "Sim"])
        self.doenca_input = QLineEdit()
        
        if self.child_data['doenca_cronica'] and self.child_data['doenca_cronica'] != "Não":
            self.doenca_combo.setCurrentIndex(1)
            self.doenca_input.setText(self.child_data['doenca_cronica'])
            self.doenca_input.setVisible(True)
        else:
            self.doenca_combo.setCurrentIndex(0)
            self.doenca_input.setVisible(False)
        
        self.doenca_combo.currentIndexChanged.connect(self.toggleDoencaInput)
        
        self.alergia_combo = QComboBox()
        self.alergia_combo.addItems(["Não", "Sim"])
        self.alergia_input = QLineEdit()
        
        if self.child_data['alergia'] and self.child_data['alergia'] != "Não":
            self.alergia_combo.setCurrentIndex(1)
            self.alergia_input.setText(self.child_data['alergia'])
            self.alergia_input.setVisible(True)
        else:
            self.alergia_combo.setCurrentIndex(0)
            self.alergia_input.setVisible(False)
        
        self.alergia_combo.currentIndexChanged.connect(self.toggleAlergiaInput)
        
        self.conversa_combo = QComboBox()
        self.conversa_combo.addItems(["Não", "Sim, presencial", "Sim, online"])
        self.conversa_combo.setCurrentText(self.child_data['conversa_monitor'])
        
        self.visita_combo = QComboBox()
        self.visita_combo.addItems(["Não", "Sim"])
        self.visita_combo.setCurrentText(self.child_data['visita'])
        
        self.fotos_combo = QComboBox()
        self.fotos_combo.addItems(["Não", "Sim"])
        self.fotos_combo.setCurrentText(self.child_data['permite_fotos'])
        
        self.obs_input = QTextEdit()
        self.obs_input.setText(self.child_data['observacoes'])
        self.obs_input.setMaximumHeight(100)
        
        # Adicionar campos ao formulário
        form_layout.addRow("Nome da Criança:", self.nome_input)
        form_layout.addRow("Idade:", self.idade_input)
        form_layout.addRow("Data de Nascimento:", self.data_nascimento)
        form_layout.addRow("Pai:", self.pai_input)
        form_layout.addRow("Mãe:", self.mae_input)
        form_layout.addRow("Outro Responsável:", self.outro_resp_input)
        form_layout.addRow("Endereço:", self.endereco_input)
        form_layout.addRow("Bairro:", self.bairro_input)
        form_layout.addRow("Cidade:", self.cidade_input)
        form_layout.addRow("É membro da Missão Atos?", self.membro_combo)
        form_layout.addRow("Já passou pelo batismo de arrependimento?", self.batizado_combo)
        form_layout.addRow("Telefone:", self.telefone_input)
        
        doenca_layout = QHBoxLayout()
        doenca_layout.addWidget(self.doenca_combo)
        doenca_layout.addWidget(self.doenca_input)
        form_layout.addRow("Apresenta doença crônica?", doenca_layout)
        
        alergia_layout = QHBoxLayout()
        alergia_layout.addWidget(self.alergia_combo)
        alergia_layout.addWidget(self.alergia_input)
        form_layout.addRow("Apresenta alguma alergia?", alergia_layout)
        
        form_layout.addRow("Gostaria de conversar com monitora?", self.conversa_combo)
        form_layout.addRow("Aceita receber visita para oração?", self.visita_combo)
        form_layout.addRow("Permite postagens de fotos?", self.fotos_combo)
        form_layout.addRow("Observações:", self.obs_input)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("Salvar")
        self.btn_save.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)
        
        layout.addLayout(buttons_layout)
    
    def toggleDoencaInput(self, index):
        self.doenca_input.setVisible(index == 1)
    
    def toggleAlergiaInput(self, index):
        self.alergia_input.setVisible(index == 1)
    
    def getChildData(self):
        return {
            'nome': self.nome_input.text(),
            'idade': self.idade_input.text(),
            'data_nascimento': self.data_nascimento.date().toString("dd/MM/yyyy"),
            'pai': self.pai_input.text(),
            'mae': self.mae_input.text(),
            'outro_responsavel': self.outro_resp_input.text(),
            'endereco': self.endereco_input.text(),
            'bairro': self.bairro_input.text(),
            'cidade': self.cidade_input.text(),
            'telefone': self.telefone_input.text(),  # Telefone adicionado
            'membro': self.membro_combo.currentText(),
            'batizado': self.batizado_combo.currentText(),
            'doenca_cronica': self.doenca_input.text() if self.doenca_combo.currentIndex() == 1 else "Não",
            'alergia': self.alergia_input.text() if self.alergia_combo.currentIndex() == 1 else "Não",
            'conversa_monitor': self.conversa_combo.currentText(),
            'visita': self.visita_combo.currentText(),
            'permite_fotos': self.fotos_combo.currentText(),
            'observacoes': self.obs_input.toPlainText(),
            'visitante': self.child_data.get('visitante', 'Não'),
             'data_cadastro': self.child_data.get('data_cadastro', datetime.datetime.now().strftime("%d/%m/%Y"))
            }