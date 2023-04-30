from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from data import db_session
from data.users import Users
from data.poems import Poems
from data.poem_tags import PoemTags

app = Flask(__name__)
app.secret_key = 'some'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(Users).get(user_id)


# Главная
@app.route("/")
def main():
    db = db_session.create_session()
    poems = (db.query(Poems.id, Poems.title, Poems.content, Poems.created_on, Users.name)
               .join(Users, Users.id == Poems.author)
               .order_by(Poems.created_on.desc())
               .all())
    poem_tags = {}
    for poem in poems:
        poem_tags[poem.id] = [i.tag for i in (db.query(PoemTags.tag)
                                                  .where(PoemTags.poem_id == poem.id)
                                                  .all())]
    return render_template("main.html", poems=poems, tags=poem_tags, user=current_user)


# Cоздание записи
@app.route("/create_new_note", methods=['POST', 'GET'])
def create_new_note():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content'].replace('\n', '<br>')
        tags = request.form.get('tags').split(',')
        db = db_session.create_session()
        poem = Poems(title=title, content=content, author=current_user.id)
        try:
            db.add(poem)
            db.flush()
            db.commit()
            for tag in tags:
                db.add(PoemTags(poem_id=poem.id, tag=tag))
            db.flush()
            db.commit()
        except:
            db.rollback()
            return "Ошибка"
    elif current_user.is_authenticated:
        return render_template("create_new_note.html", user=current_user)
    else:
        return redirect("/login")
    return redirect("/")


# Регистрация
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        hash = generate_password_hash(request.form["password"], method="pbkdf2:sha256")
        name = request.form['name']
        email = request.form['email']
        db = db_session.create_session()
        user = Users(name=name, email=email, password=hash)
        try:
            db.add(user)
            db.flush()
            db.commit()
            login_user(user)
            return redirect("/")
        except:
            db.rollback()
            return "Ошибка"
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("register.html", user=current_user)


# Страница входа
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        db = db_session.create_session()
        if email and password:
            user = db.query(Users).filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                return redirect("/")
            flash("Неверный  логин или пароль", "error")
    return render_template("login.html", user=current_user)


# Запрос на выход
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


if __name__ == '__main__':
    db_session.global_init("poems.db")
    app.run(port=8080, host='127.0.0.1')
