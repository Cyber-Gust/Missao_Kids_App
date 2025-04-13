import os
import csv
import datetime
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self):
        # Obter o caminho base do projeto
        self.base_dir = self._get_base_dir()
        
        # Definir caminhos para os arquivos CSV com caminho absoluto
        self.criancas_file = os.path.join(self.base_dir, 'data', 'criancas.csv')
        self.checkins_file = os.path.join(self.base_dir, 'data', 'checkins.csv')
        
        # Criar arquivos se não existirem
        self._create_files_if_not_exist()
        
        # Imprimir informações de debug
        print(f"Diretório base: {self.base_dir}")
        print(f"Arquivo de crianças: {self.criancas_file}")
        print(f"O arquivo existe? {os.path.exists(self.criancas_file)}")
    
    def _get_base_dir(self):
        """Determina o diretório base do projeto"""
        # Obter o diretório do arquivo atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Subir dois níveis (de src/database para a raiz do projeto)
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        return base_dir
    
    def _create_files_if_not_exist(self):
        # Criar diretório de dados se não existir
        os.makedirs(os.path.dirname(self.criancas_file), exist_ok=True)
        
        # Criar arquivo de crianças se não existir
        if not os.path.exists(self.criancas_file):
            with open(self.criancas_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['nome', 'idade', 'data_nascimento', 'pai', 'mae', 'outro_responsavel', 
                                'endereco', 'bairro', 'cidade', 'membro', 'batizado', 'doenca_cronica', 
                                'alergia', 'conversa_monitor', 'visita', 'permite_fotos', 'observacoes', 'visitante', 'telefone'])
        
        # Criar arquivo de check-ins se não existir
        if not os.path.exists(self.checkins_file):
            with open(self.checkins_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['nome', 'data_checkin', 'data_checkout', 'sala'])
    
    def add_child(self, child_data: Dict[str, Any]) -> bool:
        """Adiciona uma nova criança ao banco de dados"""
        try:
            with open(self.criancas_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(child_data.keys()))
                writer.writerow(child_data)
            return True
        except Exception as e:
            print(f"Erro ao adicionar criança: {e}")
            return False
    
    def add_visitor(self, visitor_data: Dict[str, Any]) -> bool:
        """Adiciona um visitante ao banco de dados"""
        try:
            # Imprimir dados recebidos para debug
            print("Dados do visitante recebidos:")
            for key, value in visitor_data.items():
                print(f"  {key}: {value}")
            
            # Data atual para o cadastro
            current_date = datetime.datetime.now().strftime("%d/%m/%Y")
            
            # Completar dados faltantes para o visitante
            complete_data = {
                'nome': visitor_data.get('nome', ''),
                'idade': visitor_data.get('idade', ''),
                'data_nascimento': '',
                'pai': '',
                'mae': '',
                'outro_responsavel': visitor_data.get('outro_responsavel', visitor_data.get('responsavel', '')),
                'endereco': '',
                'bairro': '',
                'cidade': '',
                'telefone': visitor_data.get('telefone', ''),  # Garantir que o telefone seja armazenado aqui
                'membro': 'Não',
                'batizado': 'Não',
                'doenca_cronica': '',
                'alergia': '',
                'conversa_monitor': 'Não',
                'visita': 'Não',
                'permite_fotos': 'Não',
                'observacoes': visitor_data.get('observacoes', 'Visitante'),
                'visitante': 'Sim',
                'data_cadastro': current_date  # Adicionar data de cadastro
            }
            
            # Imprimir dados completos para debug
            print("Dados completos do visitante a serem salvos:")
            for key, value in complete_data.items():
                print(f"  {key}: {value}")
            
            # Verificar se o arquivo existe e tem conteúdo
            if not os.path.exists(self.criancas_file) or os.path.getsize(self.criancas_file) == 0:
                # Se o arquivo não existe ou está vazio, criar com cabeçalho
                with open(self.criancas_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=list(complete_data.keys()))
                    writer.writeheader()
            else:
                # Se o arquivo já existe, verificar se precisa atualizar os cabeçalhos
                with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, [])
                
                # Se os cabeçalhos não incluem os novos campos, reescrever o arquivo
                if 'telefone' not in headers or 'data_cadastro' not in headers:
                    # Ler todos os dados existentes
                    with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        existing_data = list(reader)
                    
                    # Reescrever o arquivo com os novos cabeçalhos
                    with open(self.criancas_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=list(complete_data.keys()))
                        writer.writeheader()
                        
                        # Escrever os dados existentes com os novos campos vazios
                        for row in existing_data:
                            # Adicionar campos faltantes
                            if 'telefone' not in row:
                                row['telefone'] = ''
                            if 'data_cadastro' not in row:
                                row['data_cadastro'] = ''
                            writer.writerow(row)
            
            # Adicionar o visitante
            with open(self.criancas_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(complete_data.keys()))
                writer.writerow(complete_data)
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar visitante: {e}")
            return False
    
    def get_all_children(self):
        """Retorna todas as crianças cadastradas"""
        children = []
        
        if not os.path.exists(self.criancas_file):
            print(f"Arquivo de crianças não encontrado: {self.criancas_file}")
            return children
        
        try:
            with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Imprimir cabeçalhos para debug
                print(f"Cabeçalhos do arquivo: {reader.fieldnames}")
                
                for row in reader:
                    # Criar um novo dicionário sem campos None
                    clean_row = {}
                    for key, value in row.items():
                        if key is not None:  # Ignorar campos None
                            clean_row[key] = value
                    
                    children.append(clean_row)
            
            # Debug: imprimir número de crianças e campos disponíveis
            print(f"Total de crianças lidas: {len(children)}")
            if children:
                print("Campos disponíveis:")
                for key in children[0].keys():
                    print(f"  - {key}")
            
            return children
        except Exception as e:
            print(f"Erro ao ler arquivo de crianças: {e}")
            return []
    
    def search_children(self, search_text: str) -> List[Dict[str, Any]]:
        """Busca crianças pelo nome"""
        children = []
        try:
            if not os.path.exists(self.criancas_file):
                print(f"Arquivo de crianças não encontrado: {self.criancas_file}")
                return []
                
            with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if search_text.lower() in row['nome'].lower():
                        children.append(row)
            return children
        except Exception as e:
            print(f"Erro ao buscar crianças: {e}")
            return []    
    
    def do_checkin(self, child_name: str) -> bool:
        """Realiza o check-in de uma criança"""
        try:
            # Buscar a sala da criança com base na idade
            child = self._get_child_by_name(child_name)
            if not child:
                print(f"Criança não encontrada: {child_name}")
                return False
            
            sala = self._get_sala_by_age(child['idade'])
            
            # Verificar se o arquivo existe e tem cabeçalho
            if not os.path.exists(self.checkins_file) or os.path.getsize(self.checkins_file) == 0:
                with open(self.checkins_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['nome', 'data_checkin', 'data_checkout', 'sala'])
            
            # Registrar check-in
            with open(self.checkins_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([child_name, now, '', sala])
            return True
        except Exception as e:
            print(f"Erro ao fazer check-in: {e}")
            return False
    
    def do_checkout(self, child_name: str) -> bool:
        """Realiza o check-out de uma criança"""
        try:
            if not os.path.exists(self.checkins_file):
                print(f"Arquivo de check-ins não encontrado: {self.checkins_file}")
                return False
                
            # Ler todos os check-ins
            checkins = []
            with open(self.checkins_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Pular o cabeçalho
                for row in reader:
                    checkins.append(row)
            
            # Atualizar o check-out da criança
            updated = False
            with open(self.checkins_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['nome', 'data_checkin', 'data_checkout', 'sala'])
                
                for row in checkins:
                    if row[0] == child_name and row[2] == '':  # Se for a criança e não tiver check-out
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        row[2] = now
                        updated = True
                    writer.writerow(row)
            
            return updated
        except Exception as e:
            print(f"Erro ao fazer check-out: {e}")
            return False
    
    def is_child_checked_in(self, child_name: str) -> bool:
        """Verifica se uma criança já está em check-in"""
        try:
            if not os.path.exists(self.checkins_file):
                return False
                
            with open(self.checkins_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    if row[0] == child_name and row[2] == '':  # Nome e checkout vazio
                        return True
            return False
        except Exception as e:
            print(f"Erro ao verificar check-in: {e}")
            return False
    
    def get_checked_in_children(self) -> List[Dict[str, Any]]:
        """Retorna todas as crianças em check-in"""
        children = []
        try:
            if not os.path.exists(self.checkins_file):
                return []
                
            with open(self.checkins_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    if row[2] == '':  # Checkout vazio
                        child = self._get_child_by_name(row[0])
                        if child:
                            child['sala'] = row[3]
                            children.append(child)
            return children
        except Exception as e:
            print(f"Erro ao buscar crianças em check-in: {e}")
            return []
    
    def _get_child_by_name(self, name: str) -> Dict[str, Any]:
        """Busca uma criança pelo nome"""
        try:
            if not os.path.exists(self.criancas_file):
                return {}
                
            with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['nome'] == name:
                        return row
            return {}
        except Exception as e:
            print(f"Erro ao buscar criança por nome: {e}")
            return {}
    
    def _get_sala_by_age(self, age: str) -> str:
        """Retorna a sala com base na idade da criança"""
        try:
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
        except ValueError:
            # Se não conseguir converter para inteiro, retornar sala padrão
            print(f"Erro ao converter idade: {age}")
            return "Infantil 1"

    def delete_child(self, child_name):
        """
        Exclui uma criança do banco de dados pelo nome.
        
        Args:
            child_name (str): Nome da criança a ser excluída
            
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário
        """
        try:
            if not os.path.exists(self.criancas_file):
                return False
                
            # Carregar os dados atuais
            children = self.get_all_children()
            
            # Filtrar a lista para remover a criança com o nome especificado
            updated_children = [child for child in children if child['nome'] != child_name]
            
            # Se o tamanho das listas for o mesmo, significa que a criança não foi encontrada
            if len(children) == len(updated_children):
                return False
            
            # Obter os campos do cabeçalho
            fieldnames = []
            if updated_children:
                fieldnames = list(updated_children[0].keys())
            else:
                # Se não houver mais crianças, usar campos padrão
                fieldnames = ['nome', 'idade', 'data_nascimento', 'pai', 'mae', 'outro_responsavel',
                            'endereco', 'bairro', 'cidade', 'membro', 'batizado', 'doenca_cronica',
                            'alergia', 'conversa_monitor', 'visita', 'permite_fotos', 'observacoes',
                            'visitante', 'telefone']
            
            # Escrever a lista atualizada de volta ao arquivo
            with open(self.criancas_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_children)
            
            # Remover check-ins da criança
            self._delete_child_checkins(child_name)
            
            return True
        except Exception as e:
            print(f"Erro ao excluir criança: {e}")
            return False

    def get_child_by_name(self, name: str) -> Dict[str, Any]:
        """Busca uma criança pelo nome"""
        return self._get_child_by_name(name)

    def update_child(self, old_name: str, new_data: Dict[str, Any]) -> bool:
        """Atualiza os dados de uma criança"""
        try:
            if not os.path.exists(self.criancas_file):
                return False
                
            # Ler todas as crianças
            children = []
            with open(self.criancas_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['nome'] == old_name:
                        children.append(new_data)
                    else:
                        children.append(row)
            
            # Escrever dados atualizados
            with open(self.criancas_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for child in children:
                    writer.writerow(child)
            
            # Atualizar nome nos check-ins se necessário
            if old_name != new_data['nome']:
                self._update_checkin_name(old_name, new_data['nome'])
            
            return True
        except Exception as e:
            print(f"Erro ao atualizar criança: {e}")
            return False

    def _update_checkin_name(self, old_name: str, new_name: str) -> None:
        """Atualiza o nome da criança nos check-ins"""
        try:
            if not os.path.exists(self.checkins_file):
                return
                
            # Ler todos os check-ins
            checkins = []
            with open(self.checkins_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[0] == old_name:
                        row[0] = new_name
                    checkins.append(row)
            
            # Escrever dados atualizados
            with open(self.checkins_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for checkin in checkins:
                    writer.writerow(checkin)
        except Exception as e:
            print(f"Erro ao atualizar nome nos check-ins: {e}")

    def _delete_child_checkins(self, name: str) -> None:
        """Remove todos os check-ins da criança excluída"""
        try:
            if not os.path.exists(self.checkins_file):
                return
                
            # Ler todos os check-ins
            checkins = []
            with open(self.checkins_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[0] != name:  # Manter apenas check-ins de outras crianças
                        checkins.append(row)
            
            # Escrever dados atualizados
            with open(self.checkins_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for checkin in checkins:
                    writer.writerow(checkin)
        except Exception as e:
            print(f"Erro ao excluir check-ins: {e}")