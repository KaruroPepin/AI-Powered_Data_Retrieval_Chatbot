from flask import Flask, request, jsonify
import pandas as pd
import traceback

from client_initialization import client
from BotContext import *
from data import *

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
        
            dbschema = local_schema()
            final_query = QueryMaker(prompt_usuario, client, dbschema)
            data = local_data(final_query)

            # Convert DataFrame to a list of dictionaries
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')

            return jsonify({'classification' : 'Base de Datos', 'final_query' : final_query, 'data' : data})
        
        elif classification == "Documento":

            doc_response = read_documents(prompt_usuario, client)
            return jsonify({'classification' : 'Documento', 'respuesta' : doc_response})
        
        elif classification == "Grafico":

            # Obtener el tipo de gráfico
            partes = chart_type(prompt_usuario, client)
            partes = partes.split(',')
            char_elements = {}
            for i, parte in enumerate(partes, start=1):
                char_elements[i] = parte

            # Data
            dbschema = local_schema()
            final_query = GraphicQueryMaker(prompt_usuario, client, dbschema)
            chart_data = local_data(final_query)

             # Convert DataFrame to a list of dictionaries
            if isinstance(chart_data, pd.DataFrame):
                chart_data = chart_data.to_dict(orient='records')

            return jsonify({'classification' : 'Grafico', 'chart_type' : char_elements[1], 'chart_title' : char_elements[2], 'chart_data' : chart_data})

    except Exception as e:
        # Log the traceback to see detailed error information
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
