import os
import csv
import datetime
import shutil
from PyQt5.QtChart import QLegend  # Add this import for QLegend
from PyQt5.QtChart import QAbstractBarSeries  # Import QAbstractBarSeries
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QHBoxLayout, QWidget, QComboBox, QFileDialog, 
                            QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
                            QHeaderView, QDialog, QCalendarWidget, QDateEdit)
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QIcon, QColor, QFont, QBrush, QPen, QPainter, QLinearGradient, QGradient
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries, QPieSlice, QLineSeries, QScatterSeries, QHorizontalBarSeries, QAreaSeries
from src.database.db_manager import DatabaseManager
from src.utils.helpers import WindowStateManager

class KidsTheme:
    """Tema personalizado para gráficos do ministério infantil"""
    
    @staticmethod
    def createBaseGradient():
        """Cria um gradiente de base para o fundo do gráfico"""
        gradient = QLinearGradient()
        gradient.setStart(0, 0)
        gradient.setFinalStop(1, 1)
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(240, 249, 245))
        return gradient
    
    @staticmethod
    def setupChart(chart):
        """Configura o estilo do gráfico"""
        # Configurar o fundo do gráfico
        background_gradient = KidsTheme.createBaseGradient()
        chart.setBackgroundBrush(QBrush(background_gradient))
        
        # Configurar a borda do gráfico
        chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))
        
        # Configurar as cores do título
        chart.setTitleBrush(QBrush(QColor("#5D9B7C")))
        chart.setTitleFont(QFont("Arial", 12, QFont.Bold))
        
        # Aplicar animações
        chart.setAnimationOptions(QChart.SeriesAnimations | QChart.AllAnimations)
        chart.setAnimationDuration(1000)  # 1 segundo de animação
        
        return chart
    
    @staticmethod
    def colorPalette():
        """Retorna uma paleta de cores vibrantes para crianças"""
        return [
            QColor("#FF9AA2"),  # Rosa claro
            QColor("#FFB7B2"),  # Salmão
            QColor("#FFDAC1"),  # Pêssego
            QColor("#E2F0CB"),  # Verde claro
            QColor("#B5EAD7"),  # Menta
            QColor("#C7CEEA"),  # Lavanda
            QColor("#F2D5F8"),  # Lilás
            QColor("#FCF6BD"),  # Amarelo claro
            QColor("#A2D2FF"),  # Azul claro
            QColor("#BDE0FE"),  # Azul bebê
            QColor("#CDB4DB"),  # Roxo claro
            QColor("#FFC8DD")   # Rosa médio
        ]
class RelatoriosWindow(QMainWindow):

    def createColorfulPieChart(self, data_dict, title=""):
        """Cria um gráfico de pizza colorido com os dados fornecidos"""
        # Criar o gráfico
        chart = QChart()
        chart.setTitle(title)
        
        # Aplicar o tema personalizado
        KidsTheme.setupChart(chart)
        
        # Obter a paleta de cores
        colors = KidsTheme.colorPalette()
        
        # Criar a série de pizza
        pie_series = QPieSeries()
        
        # Adicionar os dados
        color_index = 0
        for label, value in data_dict.items():
            if value > 0:  # Adicionar apenas valores positivos
                slice = pie_series.append(f"{label} ({value})", value)
                slice.setLabelVisible(True)
                
                # Definir a cor do slice
                color = colors[color_index % len(colors)]
                slice.setBrush(QBrush(color))
                slice.setPen(QPen(Qt.white, 2))
                
                # Destacar levemente o slice
                slice.setLabelColor(QColor("#333333"))
                slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                
                # Efeito de explosão (separação) para o slice
                slice.setExploded(True)
                slice.setExplodeDistanceFactor(0.05)
                
                color_index += 1
        
        # Adicionar a série ao gráfico
        chart.addSeries(pie_series)
        
        # Configurar a legenda
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("Arial", 10))
        
        return chart

    def createColorfulBarChart(self, categories, data_dict, title=""):
        """Cria um gráfico de barras colorido com os dados fornecidos"""
        # Criar o gráfico
        chart = QChart()
        chart.setTitle(title)
        
        # Aplicar o tema personalizado
        KidsTheme.setupChart(chart)
        
        # Obter a paleta de cores
        colors = KidsTheme.colorPalette()
        
        # Criar a série de barras
        bar_series = QBarSeries()
        
        # Adicionar os dados
        color_index = 0
        for label, values in data_dict.items():
            bar_set = QBarSet(label)
            
            # Definir a cor da barra
            color = colors[color_index % len(colors)]
            bar_set.setColor(color)
            bar_set.setBorderColor(Qt.white)
            
            # Adicionar valores
            for value in values:
                bar_set.append(value)
            
            bar_series.append(bar_set)
            color_index += 1
        
        # Adicionar a série ao gráfico
        chart.addSeries(bar_series)
        
        # Configurar o eixo X (categorias)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)
        
        # Configurar o eixo Y (valores)
        axis_y = QValueAxis()
        max_value = 1  # Valor mínimo para evitar erro se não houver dados
        for values in data_dict.values():
            if values and max(values) > max_value:
                max_value = max(values)
        
        axis_y.setRange(0, max_value * 1.1)
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)
        
        # Configurar a legenda
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        return chart

    def __init__(self):
        super(RelatoriosWindow, self).__init__()
        self.db = DatabaseManager()
        
        # Diretório para armazenar relatórios
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.initUI()
        
    def initUI(self):
        # Configurar a janela
        self.setWindowTitle("Relatórios - Ministério Kids")
        self.setMinimumSize(1000, 700)
        self.setObjectName("relatoriosWindow")
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Relatórios")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            margin-bottom: 20px; 
            color: #5D9B7C; 
            font-weight: bold;
        """)
        main_layout.addWidget(title_label)
        
        # Seleção de relatório em um container estilizado
        selection_widget = QWidget()
        selection_widget.setStyleSheet("""
            background-color: #F9FCFA; 
            border: 1px solid #D5E8D4; 
            border-radius: 8px; 
            padding: 10px;
        """)
        
        # Usar um layout vertical para o container de seleção
        selection_layout = QVBoxLayout(selection_widget)
        selection_layout.setContentsMargins(15, 15, 15, 15)
        selection_layout.setSpacing(15)
        
        # Primeira linha: título e combobox
        top_row = QHBoxLayout()
        
        selection_label = QLabel("Selecione o relatório:")
        selection_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333333;
        """)
        
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Número total de crianças no culto",
            "Número por faixa etária",
            "Frequência",
            "Crianças Cadastradas",
            "Visitantes",
            "Aniversariantes do mês",
            "Crianças com alergias ou restrições",
            "Famílias que pediram visitas ou conversas"
        ])
        self.report_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #D5E8D4;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                color: #333333;
                min-width: 300px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #A8D5BA;
                background-color: #F0F9F5;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #D5E8D4;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #D5E8D4;
                selection-background-color: #FFE6CC;
                selection-color: #333333;
                background-color: white;
                padding: 5px;
            }
        """)
        self.report_combo.currentIndexChanged.connect(self.loadReport)
        
        top_row.addWidget(selection_label)
        top_row.addWidget(self.report_combo, 1)  # Dar mais espaço ao combobox
        selection_layout.addLayout(top_row)
        
        # Segunda linha: botões
        buttons_row = QHBoxLayout()
        
        # Botão para selecionar data (para relatórios históricos)
        self.btn_date = QPushButton("Selecionar Data")
        self.btn_date.setStyleSheet("""
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
        self.btn_date.clicked.connect(self.selectDate)
        
        # Botão para limpar relatórios
        self.btn_clear = QPushButton("Limpar Relatórios")
        self.btn_clear.setStyleSheet("""
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
        self.btn_clear.clicked.connect(self.clearReports)
        
        # Botão de exportar
        self.btn_export = QPushButton("Exportar para CSV")
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: #FFD8B1;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
                min-width: 150px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FFCCA0;
            }
            QPushButton:pressed {
                background-color: #FFBF8F;
            }
        """)
        
        # Tentar carregar o ícone se existir
        icon_path = "assets/icons/excel.png"
        if os.path.exists(icon_path):
            self.btn_export.setIcon(QIcon(icon_path))
            self.btn_export.setIconSize(QSize(16, 16))
        
        self.btn_export.clicked.connect(self.exportToCSV)
        
        # Data selecionada (padrão: hoje)
        self.selected_date = datetime.datetime.now().date()
        
        buttons_row.addWidget(self.btn_date)
        buttons_row.addStretch(1)  # Espaço flexível entre os botões
        buttons_row.addWidget(self.btn_clear)
        buttons_row.addWidget(self.btn_export)
        
        selection_layout.addLayout(buttons_row)
        main_layout.addWidget(selection_widget)
        
        # Tabs para tabela e gráfico
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #D5E8D4;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }
            QTabBar::tab {
                background-color: #F5F5F5;
                color: #333333;
                border: 1px solid #D5E8D4;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 25px;  /* Aumentado o padding horizontal */
                margin-right: 2px;
                font-size: 14px;
                min-width: 120px;  /* Definir largura mínima */
            }
            QTabBar::tab:selected {
                background-color: #A8D5BA;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E5F0EA;
            }
        """)
        
        # Tab de tabela
        self.table_tab = QWidget()
        table_layout = QVBoxLayout(self.table_tab)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D5E8D4;
                border-radius: 6px;
                background-color: white;
                gridline-color: #E5F0EA;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F0F0F0;
            }
            QTableWidget::item:selected {
                background-color: #FFE6CC;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #A8D5BA;
                color: #333333;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QHeaderView::section:horizontal {
                border-right: 1px solid #D5E8D4;
            }
            QTableCornerButton::section {
                background-color: #A8D5BA;
                border: none;
            }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        table_layout.addWidget(self.table)
        
        # Tab de gráfico
        self.chart_tab = QWidget()
        chart_layout = QVBoxLayout(self.chart_tab)
        chart_layout.setContentsMargins(10, 10, 10, 10)
        
        # Criar o QChartView para exibir gráficos
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)  # Use QPainter.Antialiasing em vez de QPen.Antialiasing
        self.chart_view.setMinimumHeight(400)
        chart_layout.addWidget(self.chart_view)
        
        # Adicionar tabs
        self.tabs.addTab(self.table_tab, "Tabela")
        self.tabs.addTab(self.chart_tab, "Gráfico")
        
        main_layout.addWidget(self.tabs)
        
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
        
        # Carregar relatório inicial
        self.loadReport(0)
   
    def voltarMainWindow(self):
        # Salvar o estado atual da janela
        window_manager = WindowStateManager.get_instance()
        window_manager.save_state(self)
        
        from src.interface.main_window import MainWindow
        self.main_window = MainWindow()
        # Restaurar o estado da janela
        window_manager.restore_state(self.main_window)
        self.main_window.show()
        self.close()
    
    def selectDate(self):
        """Abre um diálogo para selecionar uma data para o relatório"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Selecionar Data")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        calendar.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        
        # Definir a data atual como selecionada
        calendar.setSelectedDate(QDate(
            self.selected_date.year,
            self.selected_date.month,
            self.selected_date.day
        ))
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        
        layout.addWidget(calendar)
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            selected_date = calendar.selectedDate()
            self.selected_date = datetime.date(
                selected_date.year(),
                selected_date.month(),
                selected_date.day()
            )
            # Recarregar o relatório com a nova data
            self.loadReport(self.report_combo.currentIndex())
    
    def loadReport(self, index):
        # Obter tipo de relatório
        report_type = self.report_combo.currentText()
        
        # Carregar o relatório adequado
        if report_type == "Número total de crianças no culto":
            self.loadTotalChildrenReport()
        elif report_type == "Número por faixa etária":
            self.loadAgeGroupReport()
        elif report_type == "Frequência":
            self.loadFrequencyReport()
        elif report_type == "Crianças Cadastradas":  # Nova condição
            self.loadRegisteredChildrenReport()
        elif report_type == "Visitantes":
            self.loadVisitorsReport()
        elif report_type == "Aniversariantes do mês":
            self.loadBirthdayReport()
        elif report_type == "Crianças com alergias ou restrições":
            self.loadAllergiesReport()
        elif report_type == "Famílias que pediram visitas ou conversas":
            self.loadVisitRequestsReport()
    
    def loadTotalChildrenReport(self):
        # Obter dados do dia atual
        date_str = self.selected_date.strftime("%Y-%m-%d")
        
        # Verificar se há dados de check-in para a data selecionada
        # Primeiro, vamos tentar obter diretamente do banco de dados
        checked_in_children = []
        
        # Tentar obter check-ins do dia atual
        try:
            # Verificar se o arquivo de check-ins existe
            if os.path.exists(self.db.checkins_file):
                with open(self.db.checkins_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Verificar se a data do check-in corresponde à data selecionada
                        checkin_date = datetime.datetime.strptime(row['data_checkin'], "%Y-%m-%d %H:%M:%S").date()
                        selected_date = self.selected_date
                        
                        if checkin_date == selected_date:
                            checked_in_children.append(row)
                            print(f"Encontrado check-in para a data {selected_date}: {row['nome']}")
        except Exception as e:
            print(f"Erro ao ler check-ins: {e}")
        
        total_children = len(checked_in_children)
        print(f"Total de crianças encontradas para a data {date_str}: {total_children}")
        
        # Carregar dados históricos se disponíveis
        report_file = os.path.join(self.reports_dir, 'total_children.csv')
        historical_data = self.loadHistoricalData(report_file)
        
        # Adicionar dados atuais se ainda não existirem para a data selecionada
        date_exists = False
        for entry in historical_data:
            if entry[0] == date_str:
                date_exists = True
                break
        
        if not date_exists and total_children > 0:
            historical_data.append([date_str, str(total_children)])
            self.saveHistoricalData(report_file, historical_data)
        
        # Se não houver dados históricos e não houver check-ins para hoje,
        # adicionar uma entrada com zero para mostrar algo na tabela
        if not historical_data:
            historical_data.append([date_str, "0"])
            self.saveHistoricalData(report_file, historical_data)
        
        # Configurar tabela
        self.table.setRowCount(len(historical_data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Data", "Total de Crianças"])
        
        # Adicionar dados à tabela
        for i, (date, count) in enumerate(historical_data):
            # Converter formato de data
            display_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
            
            date_item = QTableWidgetItem(display_date)
            date_item.setTextAlignment(Qt.AlignCenter)
            
            count_item = QTableWidgetItem(count)
            count_item.setTextAlignment(Qt.AlignCenter)
            
            self.table.setItem(i, 0, date_item)
            self.table.setItem(i, 1, count_item)
        
        # Ajustar colunas
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Criar gráfico
        chart = QChart()
        chart.setTitle("Total de Crianças no Culto")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1000)  # Duração da animação em milissegundos

        # Definir estilo do título
        title_font = QFont("Arial", 12, QFont.Bold)
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

        # Definir fundo do gráfico com gradiente
        background_gradient = QLinearGradient()
        background_gradient.setStart(0, 0)
        background_gradient.setFinalStop(0, 1)
        background_gradient.setColorAt(0.0, QColor(255, 255, 255))
        background_gradient.setColorAt(1.0, QColor(240, 249, 245))
        chart.setBackgroundBrush(QBrush(background_gradient))

        # Adicionar borda ao gráfico
        chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))

        # Usar apenas os últimos 10 registros para o gráfico
        display_data = historical_data[-10:] if len(historical_data) > 10 else historical_data

        # Criar conjunto de barras com cor personalizada
        bar_set = QBarSet("Crianças")
        bar_set.setColor(QColor("#A8D5BA"))  # Verde claro
        bar_set.setBorderColor(QColor("#5D9B7C"))  # Verde escuro para a borda
        bar_set.setLabelColor(QColor("#333333"))  # Cor do texto

        categories = []

        for date, count in display_data:
            bar_set.append(int(count))
            # Converter formato de data para exibição
            display_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m")
            categories.append(display_date)

        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_series.setLabelsVisible(True)  # Mostrar rótulos
        bar_series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)  # Posição dos rótulos

        chart.addSeries(bar_series)

        # Configurar eixo X (datas)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#333333"))  # Cor do texto
        axis_x.setTitleText("Data")  # Título do eixo
        axis_x.setTitleFont(QFont("Arial", 10, QFont.Bold))
        axis_x.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)

        # Configurar eixo Y (valores)
        axis_y = QValueAxis()
        max_value = max([int(count) for _, count in display_data]) if display_data else 10
        axis_y.setRange(0, max_value + 5)
        axis_y.setLabelFormat("%d")  # Formato dos números
        axis_y.setLabelsColor(QColor("#333333"))  # Cor do texto
        axis_y.setTitleText("Número de Crianças")  # Título do eixo
        axis_y.setTitleFont(QFont("Arial", 10, QFont.Bold))
        axis_y.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)

        # Configurar legenda
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("Arial", 10))
        chart.legend().setLabelColor(QColor("#333333"))

        # Adicionar tooltip ao gráfico
        chart.setToolTip("Relatório de presença de crianças")

        self.chart_view.setChart(chart)
    
    def loadAgeGroupReport(self):
        # Obter dados
        checked_in_children = self.db.get_checked_in_children()
        
        # Adicionar mensagens de debug
        print(f"Total de crianças encontradas: {len(checked_in_children)}")
        
        # Contar por faixa etária
        age_groups = {
            "Berçário (0-2)": 0,
            "Infantil 1 (3)": 0,
            "Infantil 2 (4-5)": 0,
            "Infantil 3 (6-7)": 0,
            "Infantil 4 (8-10)": 0,
            "Juniores (11+)": 0
        }
        
        # Verificar se há crianças
        if not checked_in_children:
            print("Nenhuma criança encontrada em check-in.")
            
            # Se não houver crianças em check-in, tentar obter todas as crianças cadastradas
            all_children = self.db.get_all_children()
            print(f"Total de crianças cadastradas: {len(all_children)}")
            
            # Usar todas as crianças cadastradas se não houver check-ins
            if all_children:
                checked_in_children = all_children
        
        # Contar crianças por faixa etária
        for child in checked_in_children:
            try:
                # Tentar converter idade para inteiro
                age = int(child.get('idade', 0))
                print(f"Processando criança: {child.get('nome', 'Sem nome')} - Idade: {age}")
                
                if age <= 2:
                    age_groups["Berçário (0-2)"] += 1
                elif age == 3:
                    age_groups["Infantil 1 (3)"] += 1
                elif age <= 5:
                    age_groups["Infantil 2 (4-5)"] += 1
                elif age <= 7:
                    age_groups["Infantil 3 (6-7)"] += 1
                elif age <= 10:
                    age_groups["Infantil 4 (8-10)"] += 1
                else:
                    age_groups["Juniores (11+)"] += 1
            except (ValueError, TypeError) as e:
                # Se a idade não for um número válido, imprimir mensagem de erro
                print(f"Erro ao processar idade da criança {child.get('nome', 'Sem nome')}: {e}")
                print(f"Valor da idade: {child.get('idade', 'Não definido')} - Tipo: {type(child.get('idade', None))}")
                continue
        
        # Imprimir contagem por faixa etária
        for group, count in age_groups.items():
            print(f"{group}: {count}")
        
        # Configurar tabela
        self.table.setRowCount(len(age_groups))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Faixa Etária", "Quantidade"])
        
        # Adicionar dados à tabela
        for i, (group, count) in enumerate(age_groups.items()):
            group_item = QTableWidgetItem(group)
            group_item.setTextAlignment(Qt.AlignCenter)
            
            count_item = QTableWidgetItem(str(count))
            count_item.setTextAlignment(Qt.AlignCenter)
            
            self.table.setItem(i, 0, group_item)
            self.table.setItem(i, 1, count_item)
        
        # Ajustar colunas
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Criar gráfico
        chart = QChart()
        chart.setTitle("Crianças por Faixa Etária")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1200)  # Animação mais longa para efeito visual

        # Definir estilo do título
        title_font = QFont("Arial", 12, QFont.Bold)
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

        # Definir fundo do gráfico com gradiente
        background_gradient = QLinearGradient()
        background_gradient.setStart(0, 0)
        background_gradient.setFinalStop(0, 1)
        background_gradient.setColorAt(0.0, QColor(255, 255, 255))
        background_gradient.setColorAt(1.0, QColor(240, 249, 245))
        chart.setBackgroundBrush(QBrush(background_gradient))

        # Adicionar borda ao gráfico
        chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))

        # Verificar se há dados para exibir no gráfico
        has_data = any(count > 0 for count in age_groups.values())

        # Definir cores vibrantes para cada faixa etária
        colors = [
            QColor("#FF9AA2"),  # Rosa claro - Berçário
            QColor("#FFB7B2"),  # Salmão - Infantil 1
            QColor("#FFDAC1"),  # Pêssego - Infantil 2
            QColor("#E2F0CB"),  # Verde claro - Infantil 3
            QColor("#B5EAD7"),  # Menta - Infantil 4
            QColor("#C7CEEA"),  # Lavanda - Juniores
        ]

        if has_data:
            # Gráfico de pizza
            pie_series = QPieSeries()
            
            # Contador para cores
            color_index = 0
            
            for group, count in age_groups.items():
                if count > 0:  # Adicionar apenas grupos com crianças
                    slice = pie_series.append(f"{group} ({count})", count)
                    
                    # Definir cor do slice
                    color = colors[color_index % len(colors)]
                    slice.setBrush(QBrush(color))
                    slice.setPen(QPen(Qt.white, 2))  # Borda branca para destacar
                    
                    # Configurar rótulo
                    slice.setLabelVisible(True)
                    slice.setLabelColor(QColor("#333333"))
                    slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                    
                    # Destacar o slice (pequena explosão)
                    slice.setExploded(True)
                    slice.setExplodeDistanceFactor(0.08)
                    
                    color_index += 1
            
            chart.addSeries(pie_series)
            
            # Ajustar a legenda
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chart.legend().setFont(QFont("Arial", 10))
            chart.legend().setLabelColor(QColor("#333333"))
            
            # Adicionar interatividade - conectar sinais para quando o mouse passar sobre os slices
            for slice in pie_series.slices():
                slice.hovered.connect(lambda state, slice=slice: self.highlightPieSlice(state, slice))
        else:
            # Se não houver dados, adicionar uma mensagem ao gráfico
            no_data_series = QPieSeries()
            slice = no_data_series.append("Sem dados", 1)
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#333333"))
            slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
            chart.addSeries(no_data_series)
            
            # Adicionar uma anotação ao gráfico
            chart.setTitle("Não há dados disponíveis para exibição")

        # Definir o gráfico no QChartView
        self.chart_view.setChart(chart)

        # Salvar dados históricos
        report_file = os.path.join(self.reports_dir, 'age_groups.csv')
        date_str = self.selected_date.strftime("%Y-%m-%d")

        # Verificar se já existe um relatório para esta data
        historical_data = self.loadHistoricalData(report_file)

        # Procurar por dados da data selecionada
        data_for_date = None
        for i, row in enumerate(historical_data):
            if row[0] == date_str:
                data_for_date = row
                break

        # Se não existir, adicionar os dados atuais
        if not data_for_date and has_data:
            new_row = [date_str]
            for group, count in age_groups.items():
                new_row.append(str(count))
            historical_data.append(new_row)
            self.saveHistoricalData(report_file, historical_data, 
                                headers=["Data"] + list(age_groups.keys()))
            
    def highlightPieSlice(self, state, slice):
        """Destaca ou remove o destaque de um slice quando o mouse passa sobre ele"""
        if state:
            # Quando o mouse passa sobre o slice
            slice.setExplodeDistanceFactor(0.15)  # Aumenta a explosão
            slice.setLabelFont(QFont("Arial", 10, QFont.Bold))  # Aumenta a fonte
        else:
            # Quando o mouse sai do slice
            slice.setExplodeDistanceFactor(0.08)  # Volta ao normal
            slice.setLabelFont(QFont("Arial", 9, QFont.Bold))  # Volta ao normal
    
    def loadFrequencyReport(self):
        """Carrega o relatório de frequência das crianças"""
        print("Carregando relatório de frequência...")
        
        # Obter todas as crianças cadastradas
        all_children = self.db.get_all_children()
        print(f"Total de crianças cadastradas: {len(all_children)}")
        
        # Criar um dicionário para armazenar as frequências por criança
        frequency_data = {}
        
        # Verificar se o arquivo de check-ins existe
        if os.path.exists(self.db.checkins_file):
            try:
                # Ler todos os check-ins
                with open(self.db.checkins_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        child_name = row.get('nome', '')
                        if child_name:
                            # Inicializar o registro se ainda não existir
                            if child_name not in frequency_data:
                                frequency_data[child_name] = {
                                    'count': 0,
                                    'dates': set(),  # Conjunto para evitar contar dias duplicados
                                    'sala': row.get('sala', '')
                                }
                            
                            # Extrair a data do check-in (ignorando a hora)
                            try:
                                checkin_date = datetime.datetime.strptime(
                                    row.get('data_checkin', ''), 
                                    "%Y-%m-%d %H:%M:%S"
                                ).strftime("%Y-%m-%d")
                                
                                # Adicionar a data ao conjunto de datas
                                frequency_data[child_name]['dates'].add(checkin_date)
                                
                                # Atualizar a sala (usar a mais recente)
                                frequency_data[child_name]['sala'] = row.get('sala', '')
                            except Exception as e:
                                print(f"Erro ao processar data de check-in: {e}")
                
                # Calcular o total de frequências (número de dias diferentes)
                for name in frequency_data:
                    frequency_data[name]['count'] = len(frequency_data[name]['dates'])
                
                print(f"Dados de frequência processados para {len(frequency_data)} crianças")
            except Exception as e:
                print(f"Erro ao ler arquivo de check-ins: {e}")
        
        # Preparar dados para a tabela
        table_data = []
        for child in all_children:
            name = child.get('nome', '')
            # Obter dados de frequência se disponíveis
            frequency = frequency_data.get(name, {'count': 0, 'sala': ''})
            
            # Determinar status (membro ou visitante)
            status = "Visitante" if child.get('visitante', 'Não') == 'Sim' else "Membro"
            
            # Determinar sala com base nos dados de frequência ou na idade
            sala = frequency.get('sala', '')
            if not sala:
                try:
                    age = int(child.get('idade', 0))
                    sala = self.db._get_sala_by_age(age)
                except:
                    sala = "Não definida"
            
            # Adicionar à lista de dados
            table_data.append({
                'nome': name,
                'frequencia': frequency.get('count', 0),
                'status': status,
                'sala': sala
            })
        
        # Ordenar por frequência (decrescente) e depois por nome
        table_data.sort(key=lambda x: (-x['frequencia'], x['nome']))
        
        # Configurar tabela
        self.table.setRowCount(len(table_data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome", "Frequência", "Status", "Sala"])
        
        # Adicionar dados à tabela
        for i, data in enumerate(table_data):
            name_item = QTableWidgetItem(data['nome'])
            freq_item = QTableWidgetItem(str(data['frequencia']))
            status_item = QTableWidgetItem(data['status'])
            sala_item = QTableWidgetItem(data['sala'])
            
            # Alinhar ao centro
            freq_item.setTextAlignment(Qt.AlignCenter)
            status_item.setTextAlignment(Qt.AlignCenter)
            sala_item.setTextAlignment(Qt.AlignCenter)
            
            # Destacar visitantes
            if data['status'] == "Visitante":
                status_item.setBackground(QBrush(QColor("#FFE6CC")))
            
            # Destacar crianças com alta frequência (mais de 3 presenças)
            if data['frequencia'] > 3:
                freq_item.setBackground(QBrush(QColor("#E5F0EA")))
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, freq_item)
            self.table.setItem(i, 2, status_item)
            self.table.setItem(i, 3, sala_item)

            # Ajustar colunas
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Criar gráfico
            chart = QChart()
            chart.setTitle("Frequência por Criança")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setAnimationDuration(1200)  # Animação mais longa para efeito visual

            # Definir estilo do título
            title_font = QFont("Arial", 12, QFont.Bold)
            chart.setTitleFont(title_font)
            chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

            # Definir fundo do gráfico com gradiente
            background_gradient = QLinearGradient()
            background_gradient.setStart(0, 0)
            background_gradient.setFinalStop(0, 1)
            background_gradient.setColorAt(0.0, QColor(255, 255, 255))
            background_gradient.setColorAt(1.0, QColor(240, 249, 245))
            chart.setBackgroundBrush(QBrush(background_gradient))

            # Adicionar borda ao gráfico
            chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))

            # Verificar se há dados para exibir
            if table_data:
                # Selecionar as 10 crianças com maior frequência para o gráfico
                top_children = sorted(table_data, key=lambda x: -x['frequencia'])[:10]
                
                # Criar série de barras
                categories = []
                
                # Definir uma paleta de cores para as barras
                colors = [
                    QColor("#A8D5BA"),  # Verde claro
                    QColor("#FFB7B2"),  # Salmão
                    QColor("#FFDAC1"),  # Pêssego
                    QColor("#E2F0CB"),  # Verde claro
                    QColor("#B5EAD7"),  # Menta
                    QColor("#C7CEEA"),  # Lavanda
                    QColor("#F2D5F8"),  # Lilás
                    QColor("#FCF6BD"),  # Amarelo claro
                    QColor("#A2D2FF"),  # Azul claro
                    QColor("#BDE0FE")   # Azul bebê
                ]
                
                # Criar múltiplos barsets para usar cores diferentes
                bar_sets = []
                
                for i, child in enumerate(top_children):
                    if child['frequencia'] > 0:  # Incluir apenas crianças com frequência
                        # Criar um barset individual para cada criança para usar cores diferentes
                        bar_set = QBarSet(child['nome'])
                        bar_set.append(child['frequencia'])
                        
                        # Definir cor personalizada
                        bar_set.setColor(colors[i % len(colors)])
                        bar_set.setBorderColor(Qt.white)  # Borda branca para destacar
                        bar_set.setLabelColor(QColor("#333333"))
                        
                        bar_sets.append(bar_set)
                        categories.append(child['nome'])
                
                # Se não houver crianças com frequência, mostrar mensagem
                if not categories:
                    no_data_series = QPieSeries()
                    slice = no_data_series.append("Sem dados", 1)
                    slice.setLabelVisible(True)
                    slice.setLabelColor(QColor("#333333"))
                    slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
                    chart.addSeries(no_data_series)
                    chart.setTitle("Não há dados de frequência disponíveis")
                else:
                    # Criar série de barras horizontais
                    bar_series = QHorizontalBarSeries()
                    
                    # Adicionar todos os barsets
                    for bar_set in bar_sets:
                        bar_series.append(bar_set)
                    
                    # Configurar a série
                    bar_series.setLabelsVisible(True)  # Mostrar rótulos
                    bar_series.setLabelsPosition(QAbstractBarSeries.LabelsInsideEnd)  # Posição dos rótulos
                    bar_series.setLabelsFormat("@value")  # Formato dos rótulos
                    
                    chart.addSeries(bar_series)
                    
                    # Configurar eixos
                    axis_y = QBarCategoryAxis()
                    axis_y.append(categories)
                    axis_y.setLabelsColor(QColor("#333333"))  # Cor do texto
                    axis_y.setGridLineVisible(False)  # Remover linhas de grade
                    chart.addAxis(axis_y, Qt.AlignLeft)
                    bar_series.attachAxis(axis_y)
                    
                    axis_x = QValueAxis()
                    max_freq = max([child['frequencia'] for child in top_children]) if top_children else 1
                    axis_x.setRange(0, max_freq + 1)
                    axis_x.setTickCount(max_freq + 2)
                    axis_x.setLabelFormat("%d")  # Formato dos números
                    axis_x.setLabelsColor(QColor("#333333"))  # Cor do texto
                    axis_x.setTitleText("Número de Presenças")  # Título do eixo
                    axis_x.setTitleFont(QFont("Arial", 10, QFont.Bold))
                    axis_x.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro
                    chart.addAxis(axis_x, Qt.AlignBottom)
                    bar_series.attachAxis(axis_x)
                    
                    # Configurar legenda
                    chart.legend().setVisible(True)
                    chart.legend().setAlignment(Qt.AlignBottom)
                    chart.legend().setFont(QFont("Arial", 9))
                    chart.legend().setLabelColor(QColor("#333333"))
                    
                    # Se houver muitas crianças, ajustar o layout da legenda
                    if len(categories) > 5:
                        chart.legend().setMarkerShape(QLegend.MarkerShapeCircle)
                        chart.legend().setAlignment(Qt.AlignRight)
            else:
                # Se não houver dados, mostrar mensagem
                no_data_series = QPieSeries()
                slice = no_data_series.append("Sem dados", 1)
                slice.setLabelVisible(True)
                slice.setLabelColor(QColor("#333333"))
                slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
                chart.addSeries(no_data_series)
                chart.setTitle("Não há dados disponíveis para exibição")

            # Definir o gráfico no QChartView
            self.chart_view.setChart(chart)

            # Salvar dados históricos
            self.saveFrequencyHistoricalData(table_data)

    def saveFrequencyHistoricalData(self, table_data):
        """Salva dados históricos de frequência"""
        try:
            # Criar diretório para relatórios detalhados
            detailed_reports_dir = os.path.join(self.reports_dir, 'detailed')
            os.makedirs(detailed_reports_dir, exist_ok=True)
            
            # Nome do arquivo baseado na data atual
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            report_file = os.path.join(detailed_reports_dir, f'frequency_{date_str}.csv')
            
            # Salvar dados detalhados
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['nome', 'frequencia', 'status', 'sala'])
                writer.writeheader()
                writer.writerows(table_data)
            
            print(f"Dados de frequência salvos em {report_file}")
            
            # Também salvar um resumo para o gráfico de tendência
            summary_file = os.path.join(self.reports_dir, 'frequency_summary.csv')
            
            # Calcular totais
            total_members = sum(1 for item in table_data if item['status'] == "Membro")
            total_visitors = sum(1 for item in table_data if item['status'] == "Visitante")
            total_attendance = sum(item['frequencia'] for item in table_data)
            
            # Carregar dados históricos existentes
            historical_data = []
            if os.path.exists(summary_file):
                with open(summary_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)  # Pular cabeçalho
                    historical_data = list(reader)
            
            # Verificar se já existe um registro para a data atual
            date_exists = False
            for i, row in enumerate(historical_data):
                if row[0] == date_str:
                    # Atualizar registro existente
                    historical_data[i] = [date_str, str(total_members), str(total_visitors), str(total_attendance)]
                    date_exists = True
                    break
            
            # Adicionar novo registro se não existir
            if not date_exists:
                historical_data.append([date_str, str(total_members), str(total_visitors), str(total_attendance)])
            
            # Salvar dados resumidos
            with open(summary_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Data', 'Membros', 'Visitantes', 'Total Presenças'])
                writer.writerows(historical_data)
            
            print(f"Resumo de frequência salvo em {summary_file}")
        except Exception as e:
            print(f"Erro ao salvar dados históricos de frequência: {e}")
    
    def loadVisitorsReport(self):
        """Carrega o relatório de visitantes"""
        print("Carregando relatório de visitantes...")
        
        # Obter todas as crianças cadastradas
        all_children = self.db.get_all_children()
        print(f"Total de crianças cadastradas: {len(all_children)}")
        
        # Imprimir estrutura dos dados para debug
        if all_children:
            print("Estrutura dos dados das crianças:")
            for key in all_children[0].keys():
                print(f"  - {key}")
        
        # Filtrar apenas visitantes
        visitors = []
        for child in all_children:
            is_visitor = child.get('visitante', '').lower() == 'sim' or child.get('visitante') is True
            
            if is_visitor:
                # Imprimir dados completos do visitante para debug
                print(f"\nDados completos do visitante: {child.get('nome', 'Sem nome')}")
                for key, value in child.items():
                    print(f"  {key}: {value}")
                
                # Verificar todos os campos possíveis para o telefone
                telefone = child.get('telefone', '')
                
                # Verificar se o telefone está em um campo None
                for key, value in child.items():
                    if key is None and value:
                        print(f"  Encontrado valor em campo None: {value}")
                        if isinstance(value, list) and value:
                            telefone = value[0]
                        elif isinstance(value, str) and value:
                            telefone = value
                
                # Determinar o responsável
                responsavel = child.get('responsavel', '')
                if not responsavel:
                    mae = child.get('mae', '')
                    pai = child.get('pai', '')
                    outro_responsavel = child.get('outro_responsavel', '')
                    responsavel = outro_responsavel or mae or pai or 'Não informado'
                
                # Obter data de cadastro
                data_cadastro = child.get('data_cadastro', 'Não informada')
                
                # Adicionar à lista de visitantes
                visitors.append({
                    'nome': child.get('nome', 'Sem nome'),
                    'idade': child.get('idade', 'Não informada'),
                    'responsavel': responsavel,
                    'telefone': telefone or 'Não informado',
                    'data_cadastro': data_cadastro,
                    'observacoes': child.get('observacoes', '')
                })
        
        print(f"Total de visitantes encontrados: {len(visitors)}")
        
        # Imprimir detalhes dos visitantes para debug
        for visitor in visitors:
            print(f"Visitante: {visitor['nome']} - Telefone: {visitor['telefone']} - Data: {visitor['data_cadastro']}")
        
        # Configurar tabela
        self.table.setRowCount(len(visitors))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nome", "Idade", "Responsável", "Telefone", "Data de Cadastro"])
        
        # Adicionar dados à tabela
        for i, visitor in enumerate(visitors):
            name_item = QTableWidgetItem(visitor['nome'])
            age_item = QTableWidgetItem(visitor['idade'])
            resp_item = QTableWidgetItem(visitor['responsavel'])
            phone_item = QTableWidgetItem(visitor['telefone'])
            date_item = QTableWidgetItem(visitor['data_cadastro'])
            
            # Alinhar ao centro
            age_item.setTextAlignment(Qt.AlignCenter)
            phone_item.setTextAlignment(Qt.AlignCenter)
            date_item.setTextAlignment(Qt.AlignCenter)
            
            # Definir tooltip para mostrar observações se houver
            if visitor['observacoes']:
                name_item.setToolTip(visitor['observacoes'])
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, age_item)
            self.table.setItem(i, 2, resp_item)
            self.table.setItem(i, 3, phone_item)
            self.table.setItem(i, 4, date_item)
        
            # Ajustar colunas
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Se não houver visitantes, mostrar mensagem na tabela
            if not visitors:
                self.table.setRowCount(1)
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(["Mensagem"])
                
                message_item = QTableWidgetItem("Não há visitantes cadastrados")
                message_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, 0, message_item)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Criar gráfico
            chart = QChart()
            chart.setTitle("Visitantes vs. Membros")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setAnimationDuration(1500)  # Duração da animação em milissegundos

            # Definir estilo do título
            title_font = QFont("Arial", 12, QFont.Bold)
            chart.setTitleFont(title_font)
            chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

            # Definir fundo do gráfico com gradiente
            background_gradient = QLinearGradient()
            background_gradient.setStart(0, 0)
            background_gradient.setFinalStop(0, 1)
            background_gradient.setColorAt(0.0, QColor(255, 255, 255))
            background_gradient.setColorAt(1.0, QColor(240, 249, 245))
            chart.setBackgroundBrush(QBrush(background_gradient))

            # Adicionar borda ao gráfico
            chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))

            # Contar visitantes e membros
            total_children = len(all_children)
            visitor_count = len(visitors)
            member_count = total_children - visitor_count

            # Verificar se há dados para exibir
            if total_children > 0:
                # Gráfico de pizza
                pie_series = QPieSeries()
                
                if member_count > 0:
                    member_slice = pie_series.append(f"Membros ({member_count})", member_count)
                    member_slice.setLabelVisible(True)
                    member_slice.setLabelColor(QColor("#333333"))
                    member_slice.setLabelFont(QFont("Arial", 10, QFont.Bold))
                    member_slice.setBrush(QBrush(QColor("#A8D5BA")))  # Verde claro
                    member_slice.setPen(QPen(Qt.white, 2))  # Borda branca
                    
                    # Adicionar efeito de explosão
                    member_slice.setExploded(True)
                    member_slice.setExplodeDistanceFactor(0.05)
                
                if visitor_count > 0:
                    visitor_slice = pie_series.append(f"Visitantes ({visitor_count})", visitor_count)
                    visitor_slice.setLabelVisible(True)
                    visitor_slice.setLabelColor(QColor("#333333"))
                    visitor_slice.setLabelFont(QFont("Arial", 10, QFont.Bold))
                    visitor_slice.setBrush(QBrush(QColor("#FFB7B2")))  # Rosa salmão
                    visitor_slice.setPen(QPen(Qt.white, 2))  # Borda branca
                    
                    # Adicionar efeito de explosão
                    visitor_slice.setExploded(True)
                    visitor_slice.setExplodeDistanceFactor(0.1)  # Destacar mais os visitantes
                
                chart.addSeries(pie_series)
                
                # Adicionar legenda
                chart.legend().setVisible(True)
                chart.legend().setAlignment(Qt.AlignBottom)
                chart.legend().setFont(QFont("Arial", 10))
                chart.legend().setLabelColor(QColor("#333333"))
                
                # Adicionar interatividade - conectar sinais para quando o mouse passar sobre os slices
                for slice in pie_series.slices():
                    slice.hovered.connect(lambda state, slice=slice: self.highlightPieSlice(state, slice))
                
                # Adicionar texto com percentual
                percentual_visitantes = (visitor_count / total_children) * 100 if total_children > 0 else 0
                
                # Adicionar informações adicionais ao título
                chart.setTitle(f"Visitantes vs. Membros - Total: {total_children} crianças")
            else:
                # Se não houver dados, mostrar mensagem no gráfico
                no_data_series = QPieSeries()
                slice = no_data_series.append("Sem dados", 1)
                slice.setLabelVisible(True)
                slice.setLabelColor(QColor("#333333"))
                slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
                chart.addSeries(no_data_series)
                
                # Atualizar título
                chart.setTitle("Não há dados de visitantes disponíveis")

            # Definir o gráfico no QChartView
            self.chart_view.setChart(chart)

            # Salvar dados históricos
            self.saveVisitorsHistoricalData(visitors, member_count)

    def saveVisitorsHistoricalData(self, visitors, member_count):
        """Salva dados históricos de visitantes"""
        try:
            # Criar diretório para relatórios detalhados
            detailed_reports_dir = os.path.join(self.reports_dir, 'detailed')
            os.makedirs(detailed_reports_dir, exist_ok=True)
            
            # Nome do arquivo baseado na data atual
            date_str = self.selected_date.strftime("%Y-%m-%d")
            report_file = os.path.join(detailed_reports_dir, f'visitors_{date_str}.csv')
            
            # Salvar dados detalhados
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Nome', 'Idade', 'Responsável', 'Telefone', 'Data de Cadastro', 'Observações'])
                for visitor in visitors:
                    writer.writerow([
                        visitor['nome'],
                        visitor['idade'],
                        visitor['responsavel'],
                        visitor['telefone'],
                        visitor['data_cadastro'],
                        visitor['observacoes']
                    ])
            
            print(f"Dados de visitantes salvos em {report_file}")
            
            # Também salvar um resumo para o gráfico de tendência
            summary_file = os.path.join(self.reports_dir, 'visitors_summary.csv')
            
            # Carregar dados históricos existentes
            historical_data = []
            if os.path.exists(summary_file):
                with open(summary_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)  # Pular cabeçalho
                    historical_data = list(reader)
            
            # Verificar se já existe um registro para a data atual
            date_exists = False
            for i, row in enumerate(historical_data):
                if row[0] == date_str:
                    # Atualizar registro existente
                    historical_data[i] = [date_str, str(len(visitors)), str(member_count)]
                    date_exists = True
                    break
            
            # Adicionar novo registro se não existir
            if not date_exists:
                historical_data.append([date_str, str(len(visitors)), str(member_count)])
            
            # Salvar dados resumidos
            with open(summary_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Data', 'Visitantes', 'Membros'])
                writer.writerows(historical_data)
            
            print(f"Resumo de visitantes salvo em {summary_file}")
        except Exception as e:
            print(f"Erro ao salvar dados históricos de visitantes: {e}")

    def loadBirthdayReport(self):
        """Carrega o relatório de aniversariantes do mês"""
        print("Carregando relatório de aniversariantes do mês...")
        
        # Obter o mês atual a partir da data selecionada
        current_month = self.selected_date.month
        current_month_name = self.selected_date.strftime("%B")  # Nome do mês
        
        print(f"Buscando aniversariantes do mês {current_month} ({current_month_name})")
        
        # Obter todas as crianças cadastradas
        all_children = self.db.get_all_children()
        print(f"Total de crianças cadastradas: {len(all_children)}")
        
        # Lista para armazenar aniversariantes
        birthdays = []
        
        # Formatos de data possíveis
        date_formats = [
            "%d/%m/%Y",  # 25/12/2010
            "%Y-%m-%d",  # 2010-12-25
            "%d-%m-%Y",  # 25-12-2010
            "%m/%d/%Y",  # 12/25/2010
            "%d.%m.%Y",  # 25.12.2010
        ]
        
        # Processar cada criança
        for child in all_children:
            birth_date_str = child.get('data_nascimento', '')
            
            # Pular se não tiver data de nascimento
            if not birth_date_str or birth_date_str.strip() == '':
                continue
            
            print(f"Processando data de nascimento: {birth_date_str} para {child.get('nome', 'Sem nome')}")
            
            # Tentar diferentes formatos de data
            birth_date = None
            for date_format in date_formats:
                try:
                    birth_date = datetime.datetime.strptime(birth_date_str, date_format)
                    print(f"Data convertida com sucesso usando formato {date_format}: {birth_date}")
                    break
                except ValueError:
                    continue
            
            # Se não conseguiu converter a data, pular esta criança
            if birth_date is None:
                print(f"Não foi possível converter a data: {birth_date_str}")
                continue
            
            # Verificar se o mês de nascimento corresponde ao mês selecionado
            if birth_date.month == current_month:
                # Calcular idade atual
                today = datetime.datetime.now()
                age = today.year - birth_date.year
                # Ajustar idade se ainda não fez aniversário este ano
                if (today.month, today.day) < (birth_date.month, birth_date.day):
                    age -= 1
                
                birthdays.append({
                    'nome': child.get('nome', 'Sem nome'),
                    'data': birth_date_str,
                    'data_obj': birth_date,
                    'idade': child.get('idade', str(age)),
                    'dia': birth_date.day
                })
                
                print(f"Aniversariante encontrado: {child.get('nome', 'Sem nome')} - {birth_date.day}/{birth_date.month}")
        
        # Ordenar por dia do mês
        birthdays.sort(key=lambda x: x['dia'])
        
        print(f"Total de aniversariantes encontrados: {len(birthdays)}")
        
        # Configurar tabela
        self.table.setRowCount(len(birthdays))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome", "Data de Nascimento", "Idade", "Dia do Aniversário"])
        
        # Adicionar dados à tabela
        for i, birthday in enumerate(birthdays):
            name_item = QTableWidgetItem(birthday['nome'])
            date_item = QTableWidgetItem(birthday['data'])
            age_item = QTableWidgetItem(str(birthday['idade']))
            day_item = QTableWidgetItem(f"{birthday['dia']} de {current_month_name}")
            
            # Alinhar ao centro
            date_item.setTextAlignment(Qt.AlignCenter)
            age_item.setTextAlignment(Qt.AlignCenter)
            day_item.setTextAlignment(Qt.AlignCenter)
            
            # Destacar aniversariantes do dia atual
            today = datetime.datetime.now()
            if birthday['dia'] == today.day and current_month == today.month:
                name_item.setBackground(QBrush(QColor("#FFD8B1")))
                date_item.setBackground(QBrush(QColor("#FFD8B1")))
                age_item.setBackground(QBrush(QColor("#FFD8B1")))
                day_item.setBackground(QBrush(QColor("#FFD8B1")))
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, date_item)
            self.table.setItem(i, 2, age_item)
            self.table.setItem(i, 3, day_item)
        
            # Ajustar colunas
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Se não houver aniversariantes, mostrar mensagem na tabela
            if not birthdays:
                self.table.setRowCount(1)
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(["Mensagem"])
                
                message_item = QTableWidgetItem(f"Não há aniversariantes no mês de {current_month_name}")
                message_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, 0, message_item)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Criar gráfico
            chart = QChart()
            chart.setTitle(f"Aniversariantes do Mês {current_month_name}")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setAnimationDuration(1200)  # Duração da animação em milissegundos

            # Definir estilo do título
            title_font = QFont("Arial", 12, QFont.Bold)
            chart.setTitleFont(title_font)
            chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

            # Definir fundo do gráfico com gradiente festivo (cores de festa de aniversário)
            background_gradient = QLinearGradient()
            background_gradient.setStart(0, 0)
            background_gradient.setFinalStop(0, 1)
            background_gradient.setColorAt(0.0, QColor(255, 255, 255))
            background_gradient.setColorAt(1.0, QColor(255, 245, 250))  # Rosa muito claro
            chart.setBackgroundBrush(QBrush(background_gradient))

            # Adicionar borda ao gráfico
            chart.setBackgroundPen(QPen(QColor("#FFD8E4"), 2))  # Rosa claro para a borda

            # Verificar se há aniversariantes para exibir
            if birthdays:
                # Agrupar por semana do mês
                weeks = {
                    "Semana 1 (1-7)": 0,
                    "Semana 2 (8-14)": 0,
                    "Semana 3 (15-21)": 0,
                    "Semana 4 (22-31)": 0
                }
                
                for birthday in birthdays:
                    day = birthday['dia']
                    if day <= 7:
                        weeks["Semana 1 (1-7)"] += 1
                    elif day <= 14:
                        weeks["Semana 2 (8-14)"] += 1
                    elif day <= 21:
                        weeks["Semana 3 (15-21)"] += 1
                    else:
                        weeks["Semana 4 (22-31)"] += 1
                
                # Definir cores festivas para o gráfico de barras
                bar_colors = [
                    QColor("#FF9AA2"),  # Rosa
                    QColor("#FFDAC1"),  # Pêssego
                    QColor("#B5EAD7"),  # Menta
                    QColor("#C7CEEA")   # Lavanda
                ]
                
                # Criar múltiplos barsets para usar cores diferentes
                bar_series = QBarSeries()
                categories = []
                
                # Contador para cores
                color_index = 0
                
                for week, count in weeks.items():
                    # Criar um barset individual para cada semana
                    bar_set = QBarSet(week)
                    bar_set.append(count)
                    
                    # Definir cor personalizada
                    bar_set.setColor(bar_colors[color_index % len(bar_colors)])
                    bar_set.setBorderColor(Qt.white)  # Borda branca para destacar
                    
                    bar_series.append(bar_set)
                    categories.append(week)
                    color_index += 1
                
                # Configurar a série
                bar_series.setLabelsVisible(True)  # Mostrar rótulos
                bar_series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)  # Posição dos rótulos
                bar_series.setLabelsFormat("@value")  # Formato dos rótulos
                
                chart.addSeries(bar_series)
                
                # Configurar eixos
                axis_x = QBarCategoryAxis()
                axis_x.append(categories)
                axis_x.setLabelsColor(QColor("#333333"))  # Cor do texto
                axis_x.setGridLineVisible(False)  # Remover linhas de grade
                chart.addAxis(axis_x, Qt.AlignBottom)
                bar_series.attachAxis(axis_x)
                
                axis_y = QValueAxis()
                max_value = max(weeks.values()) if weeks.values() else 1
                axis_y.setRange(0, max_value + 1)
                axis_y.setTickCount(max_value + 2)
                axis_y.setLabelFormat("%d")  # Formato dos números
                axis_y.setLabelsColor(QColor("#333333"))  # Cor do texto
                axis_y.setTitleText("Número de Aniversariantes")  # Título do eixo
                axis_y.setTitleFont(QFont("Arial", 10, QFont.Bold))
                axis_y.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro
                chart.addAxis(axis_y, Qt.AlignLeft)
                bar_series.attachAxis(axis_y)
                
                # Configurar legenda
                chart.legend().setVisible(True)
                chart.legend().setAlignment(Qt.AlignBottom)
                chart.legend().setFont(QFont("Arial", 9))
                chart.legend().setLabelColor(QColor("#333333"))
                
                # Adicionar texto com total de aniversariantes
                total_birthdays = sum(weeks.values())
                chart.setTitle(f"Aniversariantes do Mês {current_month_name} - Total: {total_birthdays}")
            else:
                # Se não houver aniversariantes, mostrar mensagem no gráfico com estilo festivo
                no_data_series = QPieSeries()
                slice = no_data_series.append(f"Sem aniversariantes em {current_month_name}", 1)
                slice.setLabelVisible(True)
                slice.setLabelColor(QColor("#333333"))
                slice.setBrush(QBrush(QColor("#FFE6EA")))  # Rosa muito claro
                slice.setPen(QPen(QColor("#FFB7C5"), 2))  # Rosa para a borda
                chart.addSeries(no_data_series)

            # Definir o gráfico no QChartView
            self.chart_view.setChart(chart)

            # Salvar dados históricos
            self.saveBirthdayHistoricalData(birthdays, current_month, current_month_name)

    def saveBirthdayHistoricalData(self, birthdays, current_month, month_name):
        """Salva dados históricos de aniversariantes"""
        try:
            # Criar diretório para relatórios detalhados
            detailed_reports_dir = os.path.join(self.reports_dir, 'detailed')
            os.makedirs(detailed_reports_dir, exist_ok=True)
            
            # Nome do arquivo baseado no mês
            report_file = os.path.join(detailed_reports_dir, f'birthdays_{current_month}.csv')
            
            # Salvar dados detalhados
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Nome', 'Data de Nascimento', 'Idade', 'Dia'])
                for birthday in birthdays:
                    writer.writerow([
                        birthday['nome'],
                        birthday['data'],
                        birthday['idade'],
                        birthday['dia']
                    ])
            
            print(f"Dados de aniversariantes salvos em {report_file}")
            
            # Também salvar um resumo para o gráfico de tendência
            summary_file = os.path.join(self.reports_dir, 'birthdays_summary.csv')
            
            # Carregar dados históricos existentes
            historical_data = []
            if os.path.exists(summary_file):
                with open(summary_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)  # Pular cabeçalho
                    historical_data = list(reader)
            
            # Verificar se já existe um registro para o mês atual
            month_exists = False
            for i, row in enumerate(historical_data):
                if row[0] == str(current_month):
                    # Atualizar registro existente
                    historical_data[i] = [str(current_month), month_name, str(len(birthdays))]
                    month_exists = True
                    break
            
            # Adicionar novo registro se não existir
            if not month_exists:
                historical_data.append([str(current_month), month_name, str(len(birthdays))])
            
            # Salvar dados resumidos
            with open(summary_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Mês', 'Nome do Mês', 'Total de Aniversariantes'])
                writer.writerows(historical_data)
            
            print(f"Resumo de aniversariantes salvo em {summary_file}")
        except Exception as e:
            print(f"Erro ao salvar dados históricos de aniversariantes: {e}")
    
    def loadAllergiesReport(self):
        # Obter crianças com alergias ou doenças crônicas
        allergies = []
        
        for child in self.db.get_all_children():
            has_allergy = child.get('alergia') and child.get('alergia') != 'Não'
            has_disease = child.get('doenca_cronica') and child.get('doenca_cronica') != 'Não'
            
            if has_allergy or has_disease:
                allergies.append({
                    'nome': child['nome'],
                    'idade': child['idade'],
                    'alergia': child.get('alergia', 'Não') if has_allergy else 'Não',
                    'doenca': child.get('doenca_cronica', 'Não') if has_disease else 'Não'
                })
        
        # Configurar tabela
        self.table.setRowCount(len(allergies))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome", "Idade", "Alergia", "Doença Crônica"])
        
        # Adicionar dados à tabela
        for i, child in enumerate(allergies):
            name_item = QTableWidgetItem(child['nome'])
            age_item = QTableWidgetItem(child['idade'])
            allergy_item = QTableWidgetItem(child['alergia'])
            disease_item = QTableWidgetItem(child['doenca'])
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, age_item)
            self.table.setItem(i, 2, allergy_item)
            self.table.setItem(i, 3, disease_item)
        
        # Ajustar colunas
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Criar gráfico
        chart = QChart()
        chart.setTitle("Crianças com Restrições de Saúde")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1200)  # Duração da animação em milissegundos

        # Definir estilo do título
        title_font = QFont("Arial", 12, QFont.Bold)
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

        # Definir fundo do gráfico com gradiente suave
        background_gradient = QLinearGradient()
        background_gradient.setStart(0, 0)
        background_gradient.setFinalStop(0, 1)
        background_gradient.setColorAt(0.0, QColor(255, 255, 255))
        background_gradient.setColorAt(1.0, QColor(245, 250, 255))  # Azul muito claro
        chart.setBackgroundBrush(QBrush(background_gradient))

        # Adicionar borda ao gráfico
        chart.setBackgroundPen(QPen(QColor("#D4E1F5"), 2))  # Azul claro para a borda

        # Contar tipos de restrições
        only_allergy = 0
        only_disease = 0
        both = 0

        for child in allergies:
            has_allergy = child['alergia'] != 'Não'
            has_disease = child['doenca'] != 'Não'
            
            if has_allergy and has_disease:
                both += 1
            elif has_allergy:
                only_allergy += 1
            elif has_disease:
                only_disease += 1

        # Total de crianças com restrições
        total_restrictions = only_allergy + only_disease + both

        # Verificar se há dados para exibir
        if total_restrictions > 0:
            # Gráfico de pizza
            pie_series = QPieSeries()
            
            # Definir cores específicas para cada categoria
            if only_allergy > 0:
                allergy_slice = pie_series.append(f"Apenas Alergia ({only_allergy})", only_allergy)
                allergy_slice.setLabelVisible(True)
                allergy_slice.setLabelColor(QColor("#333333"))
                allergy_slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                allergy_slice.setBrush(QBrush(QColor("#FFB7B2")))  # Rosa salmão
                allergy_slice.setPen(QPen(Qt.white, 2))  # Borda branca
                
                # Adicionar efeito de explosão
                allergy_slice.setExploded(True)
                allergy_slice.setExplodeDistanceFactor(0.08)
            
            if only_disease > 0:
                disease_slice = pie_series.append(f"Apenas Doença Crônica ({only_disease})", only_disease)
                disease_slice.setLabelVisible(True)
                disease_slice.setLabelColor(QColor("#333333"))
                disease_slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                disease_slice.setBrush(QBrush(QColor("#A2D2FF")))  # Azul claro
                disease_slice.setPen(QPen(Qt.white, 2))  # Borda branca
                
                # Adicionar efeito de explosão
                disease_slice.setExploded(True)
                disease_slice.setExplodeDistanceFactor(0.08)
            
            if both > 0:
                both_slice = pie_series.append(f"Ambos ({both})", both)
                both_slice.setLabelVisible(True)
                both_slice.setLabelColor(QColor("#333333"))
                both_slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                both_slice.setBrush(QBrush(QColor("#E2F0CB")))  # Verde claro
                both_slice.setPen(QPen(Qt.white, 2))  # Borda branca
                
                # Adicionar efeito de explosão
                both_slice.setExploded(True)
                both_slice.setExplodeDistanceFactor(0.08)
            
            chart.addSeries(pie_series)
            
            # Configurar legenda
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chart.legend().setFont(QFont("Arial", 9))
            chart.legend().setLabelColor(QColor("#333333"))
            
            # Adicionar interatividade - conectar sinais para quando o mouse passar sobre os slices
            for slice in pie_series.slices():
                slice.hovered.connect(lambda state, slice=slice: self.highlightPieSlice(state, slice))
            
            # Atualizar título com informações adicionais
            chart.setTitle(f"Crianças com Restrições de Saúde - Total: {total_restrictions}")
        else:
            # Se não houver dados, mostrar mensagem no gráfico
            no_data_series = QPieSeries()
            slice = no_data_series.append("Sem restrições registradas", 1)
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#333333"))
            slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
            chart.addSeries(no_data_series)

        self.chart_view.setChart(chart)

        # Salvar dados históricos
        report_file = os.path.join(self.reports_dir, 'allergies.csv')
        date_str = self.selected_date.strftime("%Y-%m-%d")

        # Verificar se já existe um relatório para esta data
        historical_data = self.loadHistoricalData(report_file)

        # Procurar por dados da data selecionada
        data_exists = False
        for row in historical_data:
            if row[0] == date_str:
                data_exists = True
                break

        # Se não existir, adicionar os dados atuais
        if not data_exists:
            historical_data.append([date_str, str(only_allergy), str(only_disease), str(both)])
            self.saveHistoricalData(report_file, historical_data, 
                                headers=["Data", "Apenas Alergia", "Apenas Doença Crônica", "Ambos"])
    
    def loadRegisteredChildrenReport(self):
        """Carrega o relatório de crianças cadastradas (não visitantes)"""
        print("Carregando relatório de crianças cadastradas...")
        
        # Obter todas as crianças cadastradas
        all_children = self.db.get_all_children()
        print(f"Total de crianças cadastradas: {len(all_children)}")
        
        # Filtrar apenas crianças que não são visitantes
        registered_children = []
        for child in all_children:
            is_visitor = child.get('visitante', '').lower() == 'sim' or child.get('visitante') is True
            
            if not is_visitor:
                # Imprimir dados completos da criança para debug
                print(f"\nDados completos da criança: {child.get('nome', 'Sem nome')}")
                
                # Determinar a sala com base na idade
                sala = ""
                try:
                    idade = int(child.get('idade', 0))
                    if idade <= 2:
                        sala = "Berçário"
                    elif idade == 3:
                        sala = "Infantil 1"
                    elif idade <= 5:
                        sala = "Infantil 2"
                    elif idade <= 7:
                        sala = "Infantil 3"
                    elif idade <= 10:
                        sala = "Infantil 4"
                    else:
                        sala = "Juniores"
                except:
                    sala = "Não definida"
                
                # Verificar os campos de telefone disponíveis
                telefone = child.get('telefone', '')
                
                # Verificar se o telefone está em um campo None
                for key, value in child.items():
                    if key is None and value:
                        print(f"  Encontrado valor em campo None: {value}")
                        if isinstance(value, list) and value:
                            telefone = value[0]
                        elif isinstance(value, str) and value:
                            telefone = value
                
                # Determinar o responsável principal
                mae = child.get('mae', '')
                pai = child.get('pai', '')
                outro_responsavel = child.get('outro_responsavel', '')
                responsavel = mae or pai or outro_responsavel or 'Não informado'
                
                # Obter data de cadastro
                data_cadastro = child.get('data_cadastro', 'Não informada')
                
                # Adicionar à lista de crianças cadastradas
                registered_children.append({
                    'nome': child.get('nome', 'Sem nome'),
                    'idade': child.get('idade', 'Não informada'),
                    'data_nascimento': child.get('data_nascimento', 'Não informada'),
                    'responsavel': responsavel,
                    'telefone': telefone or 'Não informado',
                    'sala': sala,
                    'data_cadastro': data_cadastro,
                    'observacoes': child.get('observacoes', '')
                })
        
        print(f"Total de crianças membros encontradas: {len(registered_children)}")
        
        # Ordenar por nome
        registered_children.sort(key=lambda x: x['nome'])
        
        # Configurar tabela
        self.table.setRowCount(len(registered_children))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Idade", "Data de Nascimento", "Responsável", 
            "Telefone", "Sala", "Data de Cadastro"
        ])
        
        # Adicionar dados à tabela
        for i, child in enumerate(registered_children):
            name_item = QTableWidgetItem(child['nome'])
            age_item = QTableWidgetItem(child['idade'])
            birth_item = QTableWidgetItem(child['data_nascimento'])
            resp_item = QTableWidgetItem(child['responsavel'])
            phone_item = QTableWidgetItem(child['telefone'])
            room_item = QTableWidgetItem(child['sala'])
            date_item = QTableWidgetItem(child['data_cadastro'])
            
            # Alinhar ao centro
            age_item.setTextAlignment(Qt.AlignCenter)
            birth_item.setTextAlignment(Qt.AlignCenter)
            phone_item.setTextAlignment(Qt.AlignCenter)
            room_item.setTextAlignment(Qt.AlignCenter)
            date_item.setTextAlignment(Qt.AlignCenter)
            
            # Definir tooltip para mostrar observações se houver
            if child['observacoes']:
                name_item.setToolTip(child['observacoes'])
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, age_item)
            self.table.setItem(i, 2, birth_item)
            self.table.setItem(i, 3, resp_item)
            self.table.setItem(i, 4, phone_item)
            self.table.setItem(i, 5, room_item)
            self.table.setItem(i, 6, date_item)
        
             # Ajustar colunas
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Se não houver crianças cadastradas, mostrar mensagem na tabela
            if not registered_children:
                self.table.setRowCount(1)
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(["Mensagem"])
                
                message_item = QTableWidgetItem("Não há crianças cadastradas como membros")
                message_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, 0, message_item)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Criar gráfico
            chart = QChart()
            chart.setTitle("Distribuição por Sala")
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setAnimationDuration(1500)  # Duração da animação em milissegundos

            # Definir estilo do título
            title_font = QFont("Arial", 12, QFont.Bold)
            chart.setTitleFont(title_font)
            chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

            # Definir fundo do gráfico com gradiente
            background_gradient = QLinearGradient()
            background_gradient.setStart(0, 0)
            background_gradient.setFinalStop(0, 1)
            background_gradient.setColorAt(0.0, QColor(255, 255, 255))
            background_gradient.setColorAt(1.0, QColor(240, 249, 245))
            chart.setBackgroundBrush(QBrush(background_gradient))

            # Adicionar borda ao gráfico
            chart.setBackgroundPen(QPen(QColor("#D5E8D4"), 2))

            # Verificar se há dados para exibir
            if registered_children:
                # Contar crianças por sala
                rooms = {
                    "Berçário": 0,
                    "Infantil 1": 0,
                    "Infantil 2": 0,
                    "Infantil 3": 0,
                    "Infantil 4": 0,
                    "Juniores": 0
                }
                
                for child in registered_children:
                    sala = child['sala']
                    if sala in rooms:
                        rooms[sala] += 1
                    else:
                        rooms["Não definida"] = rooms.get("Não definida", 0) + 1
                
                # Definir cores vibrantes para cada sala
                room_colors = {
                    "Berçário": QColor("#FF9AA2"),      # Rosa claro
                    "Infantil 1": QColor("#FFB7B2"),    # Salmão
                    "Infantil 2": QColor("#FFDAC1"),    # Pêssego
                    "Infantil 3": QColor("#E2F0CB"),    # Verde claro
                    "Infantil 4": QColor("#B5EAD7"),    # Menta
                    "Juniores": QColor("#C7CEEA"),      # Lavanda
                    "Não definida": QColor("#F2D5F8")   # Lilás
                }
                
                # Gráfico de pizza
                pie_series = QPieSeries()
                
                # Adicionar apenas salas com crianças
                for room, count in rooms.items():
                    if count > 0:
                        slice = pie_series.append(f"{room} ({count})", count)
                        slice.setLabelVisible(True)
                        slice.setLabelColor(QColor("#333333"))
                        slice.setLabelFont(QFont("Arial", 9, QFont.Bold))
                        
                        # Definir cor do slice
                        if room in room_colors:
                            slice.setBrush(QBrush(room_colors[room]))
                        else:
                            slice.setBrush(QBrush(QColor("#F2D5F8")))  # Lilás para salas não definidas
                        
                        slice.setPen(QPen(Qt.white, 2))  # Borda branca
                        
                        # Adicionar efeito de explosão
                        slice.setExploded(True)
                        slice.setExplodeDistanceFactor(0.08)
                
                chart.addSeries(pie_series)
                
                # Configurar legenda
                chart.legend().setVisible(True)
                chart.legend().setAlignment(Qt.AlignBottom)
                chart.legend().setFont(QFont("Arial", 9))
                chart.legend().setLabelColor(QColor("#333333"))
                
                # Adicionar interatividade - conectar sinais para quando o mouse passar sobre os slices
                for slice in pie_series.slices():
                    slice.hovered.connect(lambda state, slice=slice: self.highlightPieSlice(state, slice))
                
                # Adicionar informações adicionais ao título
                total_children = sum(count for count in rooms.values() if count > 0)
                chart.setTitle(f"Distribuição por Sala - Total: {total_children} crianças")
            else:
                # Se não houver dados, mostrar mensagem no gráfico
                no_data_series = QPieSeries()
                slice = no_data_series.append("Sem dados", 1)
                slice.setLabelVisible(True)
                slice.setLabelColor(QColor("#333333"))
                slice.setBrush(QBrush(QColor("#E0E0E0")))  # Cinza claro
                chart.addSeries(no_data_series)

            # Definir o gráfico no QChartView
            self.chart_view.setChart(chart)

            # Salvar dados históricos
            self.saveRegisteredChildrenHistoricalData(registered_children)

    def saveRegisteredChildrenHistoricalData(self, registered_children):
        """Salva dados históricos de crianças cadastradas"""
        try:
            # Criar diretório para relatórios detalhados
            detailed_reports_dir = os.path.join(self.reports_dir, 'detailed')
            os.makedirs(detailed_reports_dir, exist_ok=True)
            
            # Nome do arquivo baseado na data atual
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            report_file = os.path.join(detailed_reports_dir, f'registered_children_{date_str}.csv')
            
            # Salvar dados detalhados
            with open(report_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Nome', 'Idade', 'Data de Nascimento', 'Responsável', 
                    'Telefone', 'Sala', 'Data de Cadastro', 'Observações'
                ])
                for child in registered_children:
                    writer.writerow([
                        child['nome'],
                        child['idade'],
                        child['data_nascimento'],
                        child['responsavel'],
                        child['telefone'],
                        child['sala'],
                        child['data_cadastro'],
                        child['observacoes']
                    ])
            
            print(f"Dados de crianças cadastradas salvos em {report_file}")
            
            # Também salvar um resumo para o gráfico de tendência
            summary_file = os.path.join(self.reports_dir, 'registered_children_summary.csv')
            
            # Contar crianças por sala
            rooms = {
                "Berçário": 0,
                "Infantil 1": 0,
                "Infantil 2": 0,
                "Infantil 3": 0,
                "Infantil 4": 0,
                "Juniores": 0,
                "Não definida": 0
            }
            
            for child in registered_children:
                sala = child['sala']
                if sala in rooms:
                    rooms[sala] += 1
                else:
                    rooms["Não definida"] += 1
            
            # Carregar dados históricos existentes
            historical_data = []
            if os.path.exists(summary_file):
                with open(summary_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)  # Pular cabeçalho
                    historical_data = list(reader)
            
            # Verificar se já existe um registro para a data atual
            date_exists = False
            for i, row in enumerate(historical_data):
                if row[0] == date_str:
                    # Atualizar registro existente
                    new_row = [date_str]
                    for room in rooms.keys():
                        new_row.append(str(rooms[room]))
                    historical_data[i] = new_row
                    date_exists = True
                    break
            
            # Adicionar novo registro se não existir
            if not date_exists:
                new_row = [date_str]
                for room in rooms.keys():
                    new_row.append(str(rooms[room]))
                historical_data.append(new_row)
            
            # Salvar dados resumidos
            with open(summary_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                header = ['Data'] + list(rooms.keys())
                writer.writerow(header)
                writer.writerows(historical_data)
            
            print(f"Resumo de crianças cadastradas salvo em {summary_file}")
        except Exception as e:
            print(f"Erro ao salvar dados históricos de crianças cadastradas: {e}")
            
    def loadVisitRequestsReport(self):
        # Obter famílias que pediram visitas ou conversas
        requests = []
        
        for child in self.db.get_all_children():
            wants_visit = child.get('visita') == 'Sim'
            wants_talk = child.get('conversa_monitor') and child.get('conversa_monitor') != 'Não'
            
            if wants_visit or wants_talk:
                requests.append({
                    'nome': child['nome'],
                    'idade': child['idade'],
                    'responsavel': child.get('mae', '') or child.get('pai', '') or child.get('outro_responsavel', ''),
                    'visita': 'Sim' if wants_visit else 'Não',
                    'conversa': child.get('conversa_monitor', 'Não')
                })
        
        # Configurar tabela
        self.table.setRowCount(len(requests))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nome", "Idade", "Responsável", "Visita", "Conversa"])
        
        # Adicionar dados à tabela
        for i, request in enumerate(requests):
            name_item = QTableWidgetItem(request['nome'])
            age_item = QTableWidgetItem(request['idade'])
            resp_item = QTableWidgetItem(request['responsavel'])
            visit_item = QTableWidgetItem(request['visita'])
            talk_item = QTableWidgetItem(request['conversa'])
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, age_item)
            self.table.setItem(i, 2, resp_item)
            self.table.setItem(i, 3, visit_item)
            self.table.setItem(i, 4, talk_item)
        
        # Ajustar colunas
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Criar gráfico
        chart = QChart()
        chart.setTitle("Solicitações de Contato")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1200)  # Duração da animação em milissegundos

        # Definir estilo do título
        title_font = QFont("Arial", 12, QFont.Bold)
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro

        # Definir fundo do gráfico com gradiente
        background_gradient = QLinearGradient()
        background_gradient.setStart(0, 0)
        background_gradient.setFinalStop(0, 1)
        background_gradient.setColorAt(0.0, QColor(255, 255, 255))
        background_gradient.setColorAt(1.0, QColor(245, 245, 255))  # Azul muito claro
        chart.setBackgroundBrush(QBrush(background_gradient))

        # Adicionar borda ao gráfico
        chart.setBackgroundPen(QPen(QColor("#D5D5E8"), 2))  # Azul claro para a borda

        # Contar tipos de solicitações
        only_visit = 0
        only_talk = 0
        both = 0

        for request in requests:
            wants_visit = request['visita'] == 'Sim'
            wants_talk = request['conversa'] != 'Não'
            
            if wants_visit and wants_talk:
                both += 1
            elif wants_visit:
                only_visit += 1
            elif wants_talk:
                only_talk += 1

        # Total de solicitações
        total_requests = only_visit + only_talk + both

        # Definir cores vibrantes para cada tipo de solicitação
        colors = [
            QColor("#A2D2FF"),  # Azul claro para visitas
            QColor("#BDE0FE"),  # Azul médio para conversas
            QColor("#CDB4DB")   # Roxo claro para ambos
        ]

        # Criar múltiplos barsets para usar cores diferentes
        bar_series = QBarSeries()
        categories = ["Apenas Visita", "Apenas Conversa", "Ambos"]
        values = [only_visit, only_talk, both]

        for i, (category, value) in enumerate(zip(categories, values)):
            # Criar um barset individual para cada categoria
            bar_set = QBarSet(f"{category} ({value})")
            bar_set.append(value)
            
            # Definir cor personalizada
            bar_set.setColor(colors[i % len(colors)])
            bar_set.setBorderColor(Qt.white)  # Borda branca para destacar
            
            bar_series.append(bar_set)

        # Configurar a série
        bar_series.setLabelsVisible(True)  # Mostrar rótulos
        bar_series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)  # Posição dos rótulos
        bar_series.setLabelsFormat("@value")  # Formato dos rótulos

        chart.addSeries(bar_series)

        # Configurar eixos
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#333333"))  # Cor do texto
        axis_x.setGridLineVisible(False)  # Remover linhas de grade
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_value = max(only_visit, only_talk, both, 1)
        axis_y.setRange(0, max_value + 1)
        axis_y.setLabelFormat("%d")  # Formato dos números
        axis_y.setLabelsColor(QColor("#333333"))  # Cor do texto
        axis_y.setTitleText("Número de Solicitações")  # Título do eixo
        axis_y.setTitleFont(QFont("Arial", 10, QFont.Bold))
        axis_y.setTitleBrush(QBrush(QColor("#5D9B7C")))  # Verde escuro
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)

        # Configurar legenda
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("Arial", 9))
        chart.legend().setLabelColor(QColor("#333333"))

        # Adicionar informações adicionais ao título
        chart.setTitle(f"Solicitações de Contato - Total: {total_requests}")

        self.chart_view.setChart(chart)

        # Salvar dados históricos
        report_file = os.path.join(self.reports_dir, 'visit_requests.csv')
        date_str = self.selected_date.strftime("%Y-%m-%d")

        # Verificar se já existe um relatório para esta data
        historical_data = self.loadHistoricalData(report_file)

        # Procurar por dados da data selecionada
        data_exists = False
        for row in historical_data:
            if row[0] == date_str:
                data_exists = True
                break

        # Se não existir, adicionar os dados atuais
        if not data_exists:
            historical_data.append([date_str, str(only_visit), str(only_talk), str(both)])
            self.saveHistoricalData(report_file, historical_data, 
                                headers=["Data", "Apenas Visita", "Apenas Conversa", "Ambos"])
    
    def loadHistoricalData(self, file_path, default_headers=None):
        """Carrega dados históricos de um arquivo CSV"""
        if not os.path.exists(file_path):
            # Se o arquivo não existir, retornar uma lista vazia
            return []
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Pular cabeçalho
                next(reader, None)
                return list(reader)
        except Exception as e:
            print(f"Erro ao carregar dados históricos: {e}")
            return []
    
    def saveHistoricalData(self, file_path, data, headers=None):
        """Salva dados históricos em um arquivo CSV"""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Escrever cabeçalho se fornecido
                if headers:
                    writer.writerow(headers)
                # Escrever dados
                writer.writerows(data)
        except Exception as e:
            print(f"Erro ao salvar dados históricos: {e}")
    
    def exportToCSV(self):
        """Exporta os dados da tabela atual para um arquivo CSV"""
        # Verificar se há dados para exportar
        if self.table.rowCount() == 0:
            QMessageBox.information(
                self, 
                "Exportação", 
                "Não há dados para exportar.",
                QMessageBox.Ok
            )
            return
        
        # Obter o tipo de relatório atual
        report_type = self.report_combo.currentText()
        
        # Criar nome de arquivo baseado no tipo de relatório
        default_filename = f"{report_type.replace(' ', '_').lower()}_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
        
        # Abrir diálogo para selecionar onde salvar o arquivo
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar para CSV",
            default_filename,
            "Arquivos CSV (*.csv)"
        )
        
        if not file_path:
            return  # Usuário cancelou
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Escrever cabeçalho
                headers = []
                for col in range(self.table.columnCount()):
                    headers.append(self.table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Escrever dados
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    writer.writerow(row_data)
            
            QMessageBox.information(
                self, 
                "Exportação", 
                f"Dados exportados com sucesso para {file_path}",
                QMessageBox.Ok
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erro", 
                f"Erro ao exportar dados: {e}",
                QMessageBox.Ok
            )
    
    def clearReports(self):
        """Limpa todos os relatórios armazenados"""
        reply = QMessageBox.question(
            self,
            "Limpar Relatórios",
            "Tem certeza que deseja limpar todos os relatórios armazenados?\n\nEsta ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Verificar se o diretório existe
                if os.path.exists(self.reports_dir):
                    # Remover todos os arquivos CSV no diretório
                    for file_name in os.listdir(self.reports_dir):
                        if file_name.endswith('.csv'):
                            file_path = os.path.join(self.reports_dir, file_name)
                            os.remove(file_path)
                
                # Recarregar o relatório atual
                self.loadReport(self.report_combo.currentIndex())
                
                QMessageBox.information(
                    self,
                    "Limpar Relatórios",
                    "Todos os relatórios foram limpos com sucesso.",
                    QMessageBox.Ok
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Erro ao limpar relatórios: {e}",
                    QMessageBox.Ok
                )
            