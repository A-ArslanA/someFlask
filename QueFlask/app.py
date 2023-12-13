from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from forms import LoginForm
import os
import sqlite3
# add flask-login + flask-migrate
# add avatar
# add search
# add admin


# передаем название файла
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# Как я понял, в новой версии БД сохраняется в папке instance. В терминал: 
# python
# >>>from app import app, db
# >>>app.app_context().push()
# >>>db.create_all()
# >>>exit()


# либо открываем flask shell, для этого в терминале:
# flask shell
# >>>from app import db
# >>>db.create_all()
# >>>exit()






class Message(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return '<Message %r>' % self.id


@login_manager.user_loader # current_user
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin): # userMixin для ф/й is_authenticated() is_active() is_anonymous() get_id() 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    password_hash = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)
    
    def check_password_notAll(self,  password):
        return password

# def getName(self):
#     return self.__user['name'] if self.__user else "No Name"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.errorhandler(401)
def not_authenticated(e):
    return render_template('error401.html'), 401


@app.route('/', methods = ['POST', 'GET'])
@app.route('/signUp', methods = ['POST', 'GET'])
def signUp():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        repeatpassword = request.form['repeatpassword']

        if password == repeatpassword:
            user = User(username = username, password_hash = password) # while without hash

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        except:
            return "An error occurred while register"

    else:
        return render_template("signUp.html")


@app.route('/login', methods = ['POST', 'GET'])
def logIn():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()

        # with sqlite3.connect("instance/app.db") as datab:
        #     cursor = datab.cursor()
        #     password = cursor.execute("SELECT password_hash FROM User WHERE username = ?", [user])
        if user and user.password_hash == form.password.data:
            login_user(user)
            return redirect("/chat")
        
        return redirect("/login")
    else:
        return render_template("login.html", form = form)


@app.route('/chat', methods = ['POST', 'GET'])
@app.route('/home', methods = ['POST', 'GET'])
@login_required # error 401
def chat():
    messages = Message.query.order_by(Message.id.desc()).all()
    if request.method == "POST":
        inputMessage = request.form['inputMessage']

        message = Message(message = inputMessage)

        try:
            db.session.add(message)
            db.session.commit()
            return redirect('/chat')
        except:
            return "An error occurred while add message"

    else:
        return render_template("chat.html", messages = messages)


@app.route('/editMessage/<int:id>', methods = ['POST', 'GET'])
def editMessage(id):
    message = Message.query.get(id)
    if request.method == "POST":
        message.message = request.form['inputMessage']

        try:
            db.session.commit()
            return redirect('/chat')
        except:
            return "An error occurred while editing"

    else:
        return render_template("editMessage.html", message = message)


@app.route('/deleteMessage/<int:id>')
def deleteMessage(id):
    message = Message.query.get_or_404(id) # just 'get' if not DB
    try:
        db.session.delete(message)
        db.session.commit()
        return redirect('/chat')
    except:
        return "An error occurred while deleting"



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")








# Проверка на запуск основного файла 
if __name__ == "__main__":
    app.run(debug=True)  
