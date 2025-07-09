from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users_db = {}

def load_users():
    users_db.clear()

    try:
        with open('new.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("id:"):
                    username = lines[i + 1].strip()
                    password = lines[i + 2].strip()
                    users_db[username] = password
                    i += 3  # Переходимо до наступного запису
                else:
                    i += 1  # Пропускаємо некоректний рядок
    except FileNotFoundError:
        pass  # Файл не існує


@app.route('/login', methods=['POST'])
def login():
    """ Обробка запиту на вхід """
    load_users()  # Завантажуємо користувачів перед перевіркою
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print('success:', username, ';', password)
    load_users()
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if users_db.get(username) == password:
        return jsonify({'message': f'Welcome, {username}!'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/register', methods=['POST'])
def register():
    """ Реєстрація нового користувача з перевіркою наявності """
    load_users()  # Завантажуємо існуючих користувачів із файлу

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print('new:', username, ';', password)
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if username in users_db:
        return jsonify({'error': 'Такий акаунт вже зареєстрований'}), 400

    # Запис у файл нового акаунту
    with open('new.txt', 'a', encoding='utf-8') as f:
        f.write(f"id: {len(users_db) + 1}\n")
        f.write(f"{username}\n")
        f.write(f"{password}\n\n")
    load_users()
    return jsonify({'message': f'Користувач {username} успішно зареєстрований'}), 201

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)