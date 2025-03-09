import os
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env

# Carrega as variáveis de ambiente do arquivo .env, se existir
load_dotenv()

class Config:
    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrao_segura')  # Chave secreta para segurança da aplicação
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')  # Modo de depuração (True/False)
    DROP_DATA_BASE = os.getenv('DROP_DATA_BASE', 'False').lower() in ('true', '1', 't')  # Dropar banco de dados ao iniciar

    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///usersfront.db')  # String de conexão do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações do SQLAlchemy

    # Configurações de autenticação e segurança
    ACESSO_MAI = os.getenv('ACESSO_MAI')  # Variável de ambiente para controle de acesso
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 't')  # Cookies de sessão seguros (HTTPS)
    SESSION_COOKIE_HTTPONLY = True  # Impede acesso ao cookie via JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Política de SameSite para cookies

    # Configurações de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_FILE = os.getenv('LOG_FILE', 'logs/web.log')  # Arquivo de log

    # Configurações de e-mail (exemplo)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Configurações específicas para diferentes ambientes
class DevelopmentConfig(Config):
    DEBUG = True
    DROP_DATA_BASE = True  # Dropa o banco de dados ao iniciar (apenas para desenvolvimento)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_usersfront.db'  # Banco de dados de desenvolvimento

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_usersfront.db'  # Banco de dados de teste
    WTF_CSRF_ENABLED = False  # Desativa CSRF para testes

class ProductionConfig(Config):
    DEBUG = False
    DROP_DATA_BASE = False  # Nunca dropa o banco de dados em produção
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Banco de dados de produção (ex: PostgreSQL)
    SESSION_COOKIE_SECURE = True  # Cookies de sessão seguros (HTTPS)

# Dicionário para facilitar a seleção da configuração
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Configuração padrão
}