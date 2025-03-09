import os
from datetime import datetime, timedelta
import shutil

# Arquivos ja processados e estruturados
# Esses arquivos servirao de entrada para o processamento
PATH_CORRENTE = os.getcwd()
# Referencias para os arquivos de upload
MAIN_PATH = os.path.abspath(PATH_CORRENTE)
UPLOAD_FOLDER = MAIN_PATH + '/static/upload'

class DashboardInfo:
    def __init__(self, titulo, imagem, nome, breadcrumb, mensagem):
        self.titulo = titulo
        self.imagem = imagem
        self.nome = nome 
        self.breadcrumb = breadcrumb
        self.mensagem = mensagem

class Arquivo:
    def __init__(self, nome, tipo, extensao) -> None:
        self.nome = nome
        self.tipo = tipo
        self.extensao = extensao

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S") 
    return current_time

def generate_secret_key(length=32):
    """Generates a secure random key of the specified length."""
    return os.urandom(length).hex()

def get_dashboard_info(current_user, titulo, breadcrumb, mensagem):
    #imagem_profile = utilidades.get_image_profile() or "/static/assets/icons/person-circle.svg"
    imagem_profile = "/static/assets/icons/person-circle.svg"
    return DashboardInfo(
        titulo=titulo,
        imagem=imagem_profile,
        nome=current_user.email,
        breadcrumb=breadcrumb,
        mensagem=mensagem
    )