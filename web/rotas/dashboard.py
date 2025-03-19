import logging
from flask import Blueprint, render_template, session, flash, request
from flask import redirect, url_for, current_app
from web import utilidades as utilidades_web
from flask_login import login_required, current_user
from logging.handlers import RotatingFileHandler
from werkzeug.security import generate_password_hash
import banco
from dao import UserDAO
import os
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__)

# Logger for dashboard_bp
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
dashboard_logger = logging.getLogger('dashboard')
dashboard_logger.setLevel(logging.DEBUG)
dashboard_handler = RotatingFileHandler('logs/dashboard.log', maxBytes=10000, backupCount=1)
dashboard_handler.setFormatter(formatter)
dashboard_logger.addHandler(dashboard_handler)

# Carrega os DAOs de usuarios e arquivos
userDAO = UserDAO(banco.db)

def handle_error(error_message):
    session.clear()  # Clear user session
    flash(error_message, category='danger')
    dashboard_logger.error(error_message)
    return redirect(url_for("auth.login"))

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    try:     
        titulo="Dashboar"
        breadcrumb="Dashboard Principal" 
        mensagem=f"Olá {current_user.username}, bem vindo a aplicação MAI."
        info_dashboard = utilidades_web.get_dashboard_info(current_user=current_user, titulo=titulo, breadcrumb=breadcrumb, mensagem=mensagem)
        return render_template('dashboard/principal.html', informacao=info_dashboard)
    except IOError as ioe:
        return handle_error(f"Erro de IO durante dashboard do usuário: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard do usuário")

@dashboard_bp.route('/profile')
@login_required
def profile():
    try: 
        titulo="Dashboar"
        breadcrumb="Profile"
        mensagem=f"Profile do Usuário"
        info_dashboard = utilidades_web.get_dashboard_info(current_user=current_user, titulo=titulo, breadcrumb=breadcrumb, mensagem=mensagem)
        return render_template('dashboard/profile.html', informacao=info_dashboard)
    except IOError as ioe:
        return handle_error(f"Erro de IO durante dashboard de configurações: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard de configurações")

@dashboard_bp.route('/update_profile', methods=['POST'])
def update_profile():
    try: 
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            profile_picture = request.files.get('profile_picture')  # Get the uploaded file

            # Validate password (if provided)
            if password and password != confirm_password:
                flash('As senhas não coincidem.', category='error')
                return redirect(url_for('dashboard.profile'))
            
             # Handle profile picture upload
            if profile_picture:
                # Ensure the uploads directory exists
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')                
                os.makedirs(upload_folder, exist_ok=True)
                upload_folder_user_id = os.path.join(upload_folder, str(current_user.id))
                os.makedirs(upload_folder_user_id, exist_ok=True)

                # Secure the filename and save the file
                filename = secure_filename(profile_picture.filename)
                filepath = os.path.join(upload_folder_user_id, filename)
                profile_picture.save(filepath)

                # Save the relative path to the database
                profile_picture_url = f"static/uploads/{current_user.id}/{filename}"
            else:
                # Keep the existing profile picture if no new file is uploaded
                profile_picture_url = current_user.profile_picture_url

            # Update user information
            current_user.name = name

            # Update password (if provided)
            if password:
                updated_user = userDAO.update_user(user_id = current_user.id, name=name, username=current_user.email, email=current_user.email, password=generate_password_hash(password), profile_picture_url=profile_picture_url)
            else:
                updated_user = userDAO.update_user(user_id = current_user.id, name=name, username=current_user.email, email=current_user.email, password=current_user.password, profile_picture_url=profile_picture_url)
            flash(f'Perfil do {updated_user.username} atualizado com sucesso!', category='success')
            return redirect(url_for('dashboard.profile'))
    except IOError as ioe:
        return handle_error(f"Erro de IO durante atualização de perfil do usuário: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard perfil do usuário")

@dashboard_bp.route('/configuracoes')
@login_required
def configuracoes():
    try: 
        titulo="Dashboar"
        breadcrumb="Configurações"
        mensagem=f"Configurações da aplicação"
        info_dashboard = utilidades_web.get_dashboard_info(current_user=current_user, titulo=titulo, breadcrumb=breadcrumb, mensagem=mensagem)
        return render_template('dashboard/configuracoes.html', informacao=info_dashboard)
    except IOError as ioe:
        return handle_error(f"Erro de IO durante dashboard de configurações: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard de configurações")

@dashboard_bp.route('/sobre')
@login_required
def sobre():
    try: 
        titulo="Dashboar"
        breadcrumb="Sobre"
        mensagem=f"Informações sobre a aplicação"
        info_dashboard = utilidades_web.get_dashboard_info(current_user=current_user, titulo=titulo, breadcrumb=breadcrumb, mensagem=mensagem)
        return render_template('dashboard/sobre.html', informacao=info_dashboard)
    except IOError as ioe:
        return handle_error(f"Erro de IO durante dashboard sobre do usuário: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard sobre do usuário")