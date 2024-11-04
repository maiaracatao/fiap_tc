from flask import Flask, request, jsonify
import pandas as pd
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Chave secreta para codificar e decodificar o token JWT
app.config['SECRET_KEY'] = 'T6}2#ot(nK+)F}3RBDNyubau'

# Função para verificar o token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')

        if not token:
            return jsonify({'erro': 'Token ausente!'}), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido!'}), 401

        return f(*args, **kwargs)
    return decorated

# Rota para login e geração do token
@app.route('/api/v1/login', methods=['POST'])
def login():
    auth = request.json

    if auth and auth.get('username') == 'tech' and auth.get('password') == 'challenge':
        token = jwt.encode(
            {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({'token': token})

    return jsonify({'erro': 'Credenciais inválidas!'}), 401

# Função para carregar dados do CSV a partir da URL
def load_csv_data(url):
    try:
        data = pd.read_csv(url, sep=";")
        return data
    except Exception as e:
        return str(e)

# Rota para "producao"
@app.route('/api/v1/producao', methods=['GET'])
@token_required
def list_producao():
    action = request.args.get('action')
    if action != 'list':
        return jsonify({"erro": "Ação especificada inválida"}), 400

    url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
    data = load_csv_data(url)

    if isinstance(data, str):
        return jsonify({"erro": data}), 500

    item_id = request.args.get('id')
    date = request.args.get('date')

    if item_id:
        try:
            item_id = int(item_id)
            data = data[data['id'] == item_id]

            if date:
                if date in data.columns:
                    data = data[['control', 'id', 'produto', date]]
                else:
                    return jsonify({"erro": f"Data '{date}' inválida. Coluna não encontrada."}), 400
        except ValueError:
            return jsonify({"erro": "Valor de 'id' inválido. Deve ser um número inteiro."}), 400
    else:
        data = data[['control', 'id', 'produto']]

    data_list = data.to_dict(orient='records')
    return jsonify(data_list)

# Rota para "processamento"
@app.route('/api/v1/processamento', methods=['GET'])
@token_required
def list_processamento():
    action = request.args.get('action')
    if action != 'list':
        return jsonify({"erro": "Ação especificada inválida"}), 400

    url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
    data = load_csv_data(url)

    if isinstance(data, str):
        return jsonify({"erro": data}), 500

    item_id = request.args.get('id')
    date = request.args.get('date')

    if item_id:
        try:
            item_id = int(item_id)
            data = data[data['id'] == item_id]

            if date:
                if date in data.columns:
                    data = data[['control', 'id', 'cultivar', date]]
                else:
                    return jsonify({"erro": f"Data '{date}' inválida. Coluna não encontrada."}), 400
        except ValueError:
            return jsonify({"erro": "Valor de 'id' inválido. Deve ser um número inteiro."}), 400
    else:
        data = data[['control', 'id', 'cultivar']]

    data_list = data.to_dict(orient='records')
    return jsonify(data_list)

# Rota para "comercializacao"
@app.route('/api/v1/comercializacao', methods=['GET'])
@token_required
def list_comercializacao():
    action = request.args.get('action')
    if action != 'list':
        return jsonify({"erro": "Ação especificada inválida"}), 400

    url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
    data = load_csv_data(url)

    if isinstance(data, str):
        return jsonify({"erro": data}), 500

    item_id = request.args.get('id')
    date = request.args.get('date')

    if item_id:
        try:
            item_id = int(item_id)
            data = data[data['id'] == item_id]

            if date:
                if date in data.columns:
                    data = data[['control', 'id', 'Produto', date]]
                else:
                    return jsonify({"erro": f"Data '{date}' inválida. Coluna não encontrada."}), 400
        except ValueError:
            return jsonify({"erro": "Valor de 'id' inválido. Deve ser um número inteiro."}), 400
    else:
        data = data[['control', 'id', 'Produto']]

    data_list = data.to_dict(orient='records')
    return jsonify(data_list)

# Rota para "importacao"
@app.route('/api/v1/importacao', methods=['GET'])
@token_required
def list_importacao():
    action = request.args.get('action')
    if action != 'list':
        return jsonify({"erro": "Ação especificada inválida"}), 400

    url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
    data = load_csv_data(url)

    if isinstance(data, str):
        return jsonify({"erro": data}), 500

    item_id = request.args.get('id')
    date = request.args.get('date')

    if item_id:
        try:
            item_id = int(item_id)
            data = data[data['Id'] == item_id]

            if date:
                if date in data.columns:
                    data = data[['Id', 'País', date]]
                else:
                    return jsonify({"erro": f"Data '{date}' inválida. Coluna não encontrada."}), 400
        except ValueError:
            return jsonify({"erro": "Valor de 'id' inválido. Deve ser um número inteiro."}), 400
    else:
        data = data[['Id', 'País']]

    data_list = data.to_dict(orient='records')
    return jsonify(data_list)

# Rota para "exportacao"
@app.route('/api/v1/exportacao', methods=['GET'])
@token_required
def list_exportacao():
    action = request.args.get('action')
    if action != 'list':
        return jsonify({"erro": "Ação especificada inválida"}), 400

    url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
    data = load_csv_data(url)

    if isinstance(data, str):
        return jsonify({"erro": data}), 500

    item_id = request.args.get('id')
    date = request.args.get('date')

    if item_id:
        try:
            item_id = int(item_id)
            data = data[data['Id'] == item_id]

            if date:
                if date in data.columns:
                    data = data[['Id', 'País', date]]
                else:
                    return jsonify({"erro": f"Data '{date}' inválida. Coluna não encontrada."}), 400
        except ValueError:
            return jsonify({"erro": "Valor de 'id' inválido. Deve ser um número inteiro."}), 400
    else:
        data = data[['Id', 'País']]

    data_list = data.to_dict(orient='records')
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
