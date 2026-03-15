from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

# Модель
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    passwd = db.Column(db.String(200), nullable=False)
    isadmin = db.Column(db.Integer, default=0)  # 0 или 1

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Роут для сохранения данных
@app.route('/save', methods=['POST'])
def reg():
    data = request.get_json()
    user_text = data.get('user', '')
    click_value = 1 if data.get('click') else 0

    entry = Entry(user=user_text, passwd=passwd_text)
    db.session.add(entry)
    db.session.commit()

    return jsonify({'status': 'ok', 'id': entry.id})

if __name__ == '__main__':
    app.run(debug=True)