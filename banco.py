from flask_sqlalchemy import SQLAlchemy
import sys
from sqlalchemy import ForeignKey

# componente de banco de dados
db = SQLAlchemy()

user_files = db.Table('user_files', 
    db.Column('user_id', db.Integer(), ForeignKey('users.id')), 
    db.Column('file_id', db.Integer(), ForeignKey('files.id')) 
)

# Cria as tabelas do banco
def create_tables(app, drop_data_base):
    try:
        with app.app_context():
            print('Carrega as tabelas do banco')
            if drop_data_base: 
                db.drop_all()
                db.create_all()
                db.session.commit()
                print("Banco criado com sucesso!")
            else:
                print('Tabelas carregadas com sucesso!')
    except Exception as ex:
        print(f'Erro ao carregar o banco! {str(ex)}')
        sys.exit(1)