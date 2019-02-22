from flask import request, render_template, Flask, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user, logout_user


from Forms.Form import SignupForm

from models import db, User

app = Flask(__name__)
app.secret_key = 'aabraKadaabra'
DEBUG = True



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()

                login_user(newuser)
                flash("Login is successful")
                return redirect(url_for('index'))
        else:
            return "Form didn't validate"

@app.route('/login', methods=['GET','POST'])
def login():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return "User logged in"
                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
    else:
        return "form not validated"

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()

@app.route('/protected')
@login_required
def protected():
    return "protected area"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"


def init_dB():
    db.init_app(app)
    db.app = app
    db.create_all()


if __name__ == '__main__':
    #app.init_dB()
    app.run()
