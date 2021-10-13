from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3


app = Flask(__name__)


#конектимся к базе данных в данном случае с названием list of clients
db = sqlite3.connect('list of clients', check_same_thread=False)
#для работы с базой данных
sql = db.cursor()
#создание базы данных users объявления её столбцов и опредления информации, которая будет содерджаться в них
sql.execute("""CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT
)""")
#Сохранения наших изменений в нашей базе данных, обязательно всегда!!!!
db.commit()


@app.route('/create-user', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":

        user = request.form['user']
        password = request.form['password']

        sql.execute(f"SELECT login FROM users WHERE login = '{user}'")
        # если такого логина нет в таблице
        if sql.fetchone() is None:
            # добавляем в таблицу в первую колонку переменные user_login, user_password и начальный balance
            sql.execute(f'INSERT INTO users VALUES (?, ?)', (user, password))
            db.commit()
            flash('Вы зарегистрирвались', category='success')
        #else:
            #flash("Ошибка в отправке", category='error')
        return redirect('/user')
    else:
        return render_template("create-user.html")


@app.route('/profile/<path:user>')
def profile():
    return render_template("profile.html")


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


#@app.route('/user/<int:id>')
#def rega(id):
    #userpass = Userpass.query.get(id)
    #return render_template("homeid.html", userpass=userpass)


@app.route('/user', methods=['POST', 'GET'])
def about():
    if request.method == "POST" or request.method == "GET":
        user = request.form['user']
        password = request.form['password']
        print(user, password)
        #берём столбцы login, password из таблице users, если  login= ввёденому значения в поле логин на сайте и password = ввёденому значения в поле пароль на сайте
        sql.execute(f"SELECT login, password FROM users WHERE login = '{user}' and password ='{password}'")
        # если такого логина нет отправляем на регестрацию или предлагаем ввести снова его дальше проверяем пароль
        if sql.fetchall() is None:
            about()
        else:
            user_login = request.form['user']
            print("Соси лапу")
        return redirect("/profile")
    else:
        return render_template("user.html")


@app.route('/trys')
def trys():
    return render_template("try.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)