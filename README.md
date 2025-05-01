Ministério Kids - Sistema de Gerenciamento para Ministério Infantil
🏠 🧒 👦 👧 📊 📷 🔄

Descrição
O Ministério Kids é um sistema completo para gerenciamento de ministério infantil em igrejas evangélicas. Desenvolvido com Python e PyQt5, oferece uma interface amigável para cadastro de crianças, check-in/check-out, relatórios estatísticos e galeria de imagens.

Principais Funcionalidades

🔄 Check-in/Check-out: Controle rápido de entrada e saída das crianças com busca por nome
📝 Cadastro Completo: Registro detalhado das crianças com informações de contato e saúde
📊 Relatórios Visuais: Gráficos coloridos e interativos para análise de frequência e estatísticas
📷 Galeria de Imagens: Armazenamento e visualização de fotos de eventos e atividades
💾 Banco de Dados Local: Armazenamento seguro em arquivos CSV sem necessidade de servidor

Estrutura do Projeto

ministerio_kids/
├── main.py
├── src/
│   ├── __init__.py
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── checkin.py
│   │   ├── cadastro.py
│   │   ├── relatorios.py
│   │   └── galeria.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── assets/
│   ├── icons/
│   │   ├── checkin.png
│   │   └── logo.png
│   └── styles/
│       └── estilo.qss
├── data/
│   ├── criancas.csv
│   └── checkins.csv
├── requirements.txt
└── README.md

Módulos Principais

🔄 Check-in/Check-out
Sistema intuitivo para registrar a entrada e saída das crianças, com identificação da sala correspondente à idade. Permite busca rápida por nome e registro de visitantes sem cadastro prévio.

📝 Cadastro
Formulário completo para registro de crianças com campos para:

Informações pessoais (nome, idade, data de nascimento)
Contatos dos responsáveis
Restrições alimentares e alergias
Condições médicas
Observações especiais

📊 Relatórios
Visualização estatística com gráficos coloridos e interativos:

Total de crianças por culto
Distribuição por faixa etária
Frequência individual
Aniversariantes do mês
Visitantes vs. membros
Crianças com restrições de saúde
Solicitações de visita/contato

📷 Galeria
Organização de fotos de eventos e atividades do ministério, com categorização e visualização em modo apresentação.

Descrição para Commit
Ministério Kids - Sistema de Gerenciamento para Ministério Infantil 🧒👦👧

Um aplicativo desktop completo desenvolvido em Python e PyQt5 para gerenciamento 
de ministério infantil em igrejas evangélicas. O sistema oferece funcionalidades 
de check-in/check-out, cadastro de crianças, relatórios estatísticos com gráficos 
coloridos e interativos, e galeria de imagens.

Principais recursos:
- 🖥️ Interface amigável e intuitiva
- 📝 Cadastro completo com informações de contato e saúde
- 🔄 Sistema de check-in/check-out com busca por nome
- 📊 Relatórios visuais com gráficos personalizados
- 💾 Banco de dados local em CSV sem necessidade de servidor
- 📷 Galeria para armazenamento e visualização de fotos

Ideal para igrejas de qualquer tamanho que desejam organizar seu ministério infantil
de forma eficiente e segura.
