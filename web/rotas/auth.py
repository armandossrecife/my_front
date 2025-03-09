import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from forms import LoginForm, RegisterForm
import banco
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from logging.handlers import RotatingFileHandler
from entidades import User
from dao import UserDAO

auth_bp = Blueprint('auth', __name__)

# Logger for auth_bp
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
auth_logger = logging.getLogger('auth')
auth_logger.setLevel(logging.DEBUG)
auth_handler = RotatingFileHandler('logs/auth.log', maxBytes=10000, backupCount=1)
auth_handler.setFormatter(formatter)
auth_logger.addHandler(auth_handler)

# Carrega os DAOs de usuarios e arquivos
userDAO = UserDAO(banco.db)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = userDAO.user_by_username(username)
        if not user:
            flash("Usuário não existe, tente novamente.", category='danger')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(user.password, password):
            flash('Senha incorreta, tente novamente.', category='danger') 
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Login realizado com sucesso!', category='success')
        return redirect(url_for("dashboard.dashboard", id=user.id, nome_usuario=username))
    return render_template('auth/login.html', form=login_form)

@auth_bp.route("/registro", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = register_form.name.data
        username = register_form.username.data
        password = register_form.password.data
        user = userDAO.user_by_username(username)
        if user:
            flash(f"Usuário {username} já registrado.", category='danger')
            return redirect(url_for("auth.register"))

        hash_and_salted_password = generate_password_hash(password)
        usuario = User(name=name, username=username, email=username, password=hash_and_salted_password)
        userDAO.create_user(user=usuario)
        flash('Novo usuário criado com sucesso!', category='success')
        return redirect(url_for("auth.login"))
    return render_template("auth/registro.html", form=register_form)

@auth_bp.route('/esqueci', methods=['GET', 'POST'])
def esqueci():
    if request.method == 'POST':
        flash("Funcionalidade de recuperação de senha não implementada.", category='warning')
        return redirect(url_for("auth.login"))
    return render_template('auth/esqueci.html')

@auth_bp.route('/logout') 
@login_required
def logout():
    username = session.get('username', 'Usuário')
    mensagem = f"Sessão do usuário {username} encerrada com sucesso!"
    logout_user()
    session.clear()
    flash(mensagem, category='success')
    return redirect(url_for('auth.login'))