from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- МОДЕЛЬ (таблица) ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Создаём таблицы
with app.app_context():
    db.create_all()

# --- РОУТЫ ---

# Главная — список пользователей
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Добавить пользователя (POST)
@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()

    if username and email:
        # Проверяем что email не занят
        existing = User.query. (email=email).first()
        if not existing:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()   

    return redirect(url_for('index'))

# Удалить пользователя
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 

    calculate 