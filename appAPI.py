from flask import Flask, request, jsonify
import pandas as pd
import traceback

from BotContext import *
from main import *

from client_initialization import client

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    prompt_usuario = data.get('query')


    if not prompt_usuario:
        return jsonify({'error': 'Query not provided'}), 400
    
    try:
        classification = ContextClassifier(prompt_usuario, client)

        if classification == "Base de Datos":
        
            final_query, data = database_search(prompt_usuario)

            # Convert DataFrame to a list of dictionaries
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')

            return jsonify({'classification' : 'Base de Datos', 'final_query' : final_query, 'data' : data})
        
        elif classification == "Documento":

            doc_response = document_search(prompt_usuario)
            return jsonify({'classification' : 'Documento', 'respuesta' : doc_response})




    except Exception as e:
        # Log the traceback to see detailed error information
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
