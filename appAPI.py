from flask import Flask, request, jsonify
from client_initialization import client
from BotContext import QueryMaker
from data import data

app = Flask(__name__)

def initialize_bot(prompt_usuario):
    dbschema = data()
    messages = QueryMaker(prompt_usuario, client, dbschema)
    return messages

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    prompt_usuario = data.get('query')
    
    if not prompt_usuario:
        return jsonify({'error': 'Query not provided'}), 400
    
    try:
        response = initialize_bot(prompt_usuario)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
