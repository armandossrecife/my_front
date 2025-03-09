import logging
from flask import Blueprint, render_template, session, flash
from flask import redirect, url_for
from web import utilidades as utilidades_web
from flask_login import login_required, current_user
from logging.handlers import RotatingFileHandler

dashboard_bp = Blueprint('dashboard', __name__)

# Logger for dashboard_bp
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
dashboard_logger = logging.getLogger('dashboard')
dashboard_logger.setLevel(logging.DEBUG)
dashboard_handler = RotatingFileHandler('logs/dashboard.log', maxBytes=10000, backupCount=1)
dashboard_handler.setFormatter(formatter)
dashboard_logger.addHandler(dashboard_handler)

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

@dashboard_bp.route('/sobre')
@login_required
def sobre():
    try: 
        titulo="Dashboar"
        breadcrumb="Sobre"
        mensagem=f"Olá {current_user.username}, , bem vindo ao MAI."
        info_dashboard = utilidades_web.get_dashboard_info(current_user=current_user, titulo=titulo, breadcrumb=breadcrumb, mensagem=mensagem)
        return render_template('dashboard/sobre.html', informacao=info_dashboard)
    except IOError as ioe:
        return handle_error(f"Erro de IO durante dashboard sobre do usuário: {str(ioe)}.")
    except Exception as ex:
        return handle_error(f"Erro {str(ex)} no acesso ao dashboard sobre do usuário")