from flask import Flask, request, jsonify
import json

app = Flask(__name__)

try:
    with open('database.json', 'r') as file:
        DB = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    DB = {}

@app.route('/add', methods=['POST'])
def add_name():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if name is None or age is None:
        return jsonify({"error": "Nome e idade são campos obrigatórios"}), 400

    if name in DB:
        return jsonify({"error": "Já existe esse nome"}), 400

    DB[name] = age

    with open('database.json', 'w') as file:
        json.dump(DB, file, indent=4)

    return jsonify({"message": "Nome adicionado com sucesso"}), 201

@app.route('/remove/<string:name>', methods=['DELETE'])
def remove_name(name):
    if name in DB:
        del DB[name]

        with open('database.json', 'w') as file:
            json.dump(DB, file, indent=4)

        return jsonify({"message": f"{name} foi removido da database"}), 200
    else:
        return jsonify({"error": f"{name} não foi encontrado na database"}), 404

@app.route('/DB', methods=['GET'])
def get_database():
    return jsonify(DB), 200

if __name__ == '__main__':
    app.run(debug=True)
