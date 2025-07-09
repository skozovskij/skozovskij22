from flask import Flask, request, jsonify

app = Flask(name)

users_db = {}

@app.route('/registerBtn', methods=['POST'])
def registerBtn():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if username in users_db:
        return jsonify({'error': 'User already exists'}), 400

    users_db[username] = password  # Зберігаємо користувача
    return jsonify({'message': f'User {username} registered successfully'}), 201

@app.route('/loginBtn', methods=['POST'])
def loginBtn():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    saved_password = users_db.get(username)

    if saved_password is None or saved_password != password:
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': f'User {username} logged in successfully'}), 200

if name == 'main':
    app.run(host='127.0.0.1', port=5500)