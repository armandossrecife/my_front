import os
import logging
from config import Config
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash, request
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from web.rotas import dashboard
from web.rotas import auth
import banco
from dao import UserDAO, FilesDAO
from web import utilidades as utilidades_web
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

# Cria a aplicação (web) principal
web_app = Flask(__name__, static_folder='static')
STATIC_PATH = os.path.join(web_app.root_path, 'static')
PATH_APLICACAO = web_app.root_path

# Carrega as configurações
web_app.config.from_object(Config)

# Configura o log de debug da aplicação para o arquivo web.log
# Configure the root logger (optional, for general logs)
web_app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create a file handler for the root logger
file_handler = RotatingFileHandler(filename='logs/web_app.log', maxBytes=10000, backupCount=1)
file_handler.setFormatter(formatter)
web_app.logger.addHandler(file_handler)

# Carrega uma intancia para manipular envio de e-mail
mail = Mail(web_app)

# Inicializa a instância do banco de dados
banco.db.init_app(web_app)
banco.create_tables(web_app, Config.DROP_DATA_BASE)
#banco.create_tables(web_app, True)

# Para controle de login do usuário
login_manager = LoginManager()
login_manager.init_app(web_app)
login_manager.login_view = "login"

# Carrega os DAOs de usuários e arquivos
userDAO = UserDAO(banco.db)
filesDAO = FilesDAO(banco.db)

def generate_reset_token(user_id):
    serializer = URLSafeTimedSerializer(web_app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(web_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return userDAO.user_by_id(user_id=user_id)

@login_manager.user_loader 
def load_user(user_id):
    return userDAO.user_by_id(user_id)

@login_manager.unauthorized_handler 
def unauthorized_callback():
    return redirect(url_for("auth.login"))

# Registra os Blueprints
try: 
    web_app.register_blueprint(auth.auth_bp)
    web_app.register_blueprint(dashboard.dashboard_bp)
except Exception as ex:
    web_app.logger.error(f"Erro durante o registro dos blueprints: {str(ex)}")

# Print the list of available routes
web_app.logger.info(f"Path da aplicação web: {PATH_APLICACAO}")
web_app.logger.info("List of available routes: ")
web_app.logger.info(web_app.url_map)
print("Current Time:", utilidades_web.get_current_time()) 

@web_app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@web_app.route('/')
def index():
    return render_template('index.html')

# Páginas de tratamento de erros
@web_app.errorhandler(400)
def page_bad_request(error):
    web_app.logger.error(f"Page bad request: {str(error)}")
    return render_template('erros/400.html', erro=error), 400

@web_app.errorhandler(401)
def page_unauthorized(error):
    web_app.logger.error(f"Page unauthorized: {str(error)}")
    return render_template('erros/401.html', erro=error), 401

@web_app.errorhandler(403)
def page_forbidden(error):
    web_app.logger.error(f"Page forbidden: {str(error)}")
    return render_template('erros/403.html', erro=error), 403

@web_app.errorhandler(404)
def page_not_found(error):
    web_app.logger.error(f"Page not found: {str(error)}")
    return render_template('erros/404.html', erro=error), 404

@web_app.errorhandler(500)
def internal_server_error(error):
    web_app.logger.error(f"Internal Server Error: {str(error)}")
    return render_template('erros/500.html', erro=error), 500

@web_app.errorhandler(502)
def internal_server_error_bad_gateway(error):
    web_app.logger.error(f"Internal Server Error Bad Gateway: {str(error)}")
    return render_template('erros/502.html', erro=error), 502

@web_app.errorhandler(503)
def internal_server_error_service_unavailable(error):
    web_app.logger.error(f"Internal Server Error Service Unavailable: {str(error)}")
    return render_template('erros/503.html', erro=error), 503

@web_app.errorhandler(504)
def internal_server_error_gateway_timeout(error):
    web_app.logger.error(f"Internal Server Gateway Timeout: {str(error)}")
    return render_template('erros/504.html', erro=error), 504

@web_app.route('/forgot-password', methods=['GET', 'POST'])
def esqueci():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            # Check if the email exists in your database (pseudo-code)
            user = userDAO.user_by_email(email=email)
            if user:
                # Generate a password reset token (pseudo-code)
                token = generate_reset_token(user.id)
                                
                # Send the password reset email
                reset_url = url_for('reset_password', token=token, _external=True)
                print(reset_url)
                msg = Message('Password Reset Request', sender='no-reply@example.com', recipients=[email])
                msg.body = f'''To reset your password, visit the following link:
                                {reset_url}

                                If you did not make this request, simply ignore this email.
                                '''
                mail.send(msg)
                
                flash('Foi enviado um link para o seu e-mail para resetar sua senha.', category='info')
                return redirect(url_for('auth.login'))
            else:
                flash('Email não cadastrado.', category='warning')                
        except IOError as ioe:
            flash(f"Erro de IO durante recuperação de senha do usuário: {str(ioe)}.", category='error')
        except Exception as ex:
            flash(f"Erro {str(ex)} na recuperação de senha do usuário", category='error')
        return redirect(url_for("auth.login"))
        
    return render_template('auth/esqueci.html')

# TODO: implementar o tratamento das possiveis excecoes
@web_app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_token(token)
    if not user:
        flash('Invalid or expired token.', category='error')
        return redirect(url_for('auth.esqueci'))
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password == confirm_password:
            # Update the user's password
            updated_user = userDAO.update_password(user_id=user.id, new_password=generate_password_hash(new_password))
            if updated_user: 
                flash('Sua senha foi resetada com sucesso!.', category='success')
            else:
                flash('Não retornou um usuário válido', category='error')
            return redirect(url_for('auth.login'))
        else:
            flash('Passwords do not match.', category='error')
    
    return render_template('auth/reset_password.html', token=token)

if __name__ == '__main__':
    web_app.run(debug=Config.DEBUG, port=5001)