from flask import Flask, request, jsonify
from client_initialization import client
from BotContext import QueryMaker
from data import *
# import traceback

app = Flask(__name__)

def initialize_bot(prompt_usuario):
    dbschema = local_schema()
    final_query = QueryMaker(prompt_usuario, client, dbschema)
    data = local_data(final_query)
    return final_query, data

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    prompt_usuario = data.get('query')
    
    if not prompt_usuario:
        return jsonify({'error': 'Query not provided'}), 400
    
    try:
        final_query, data = initialize_bot(prompt_usuario)
        
        # Convert DataFrame to a list of dictionaries
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')

        return jsonify({'final_query' : final_query, 'data' : data})
    

    except Exception as e:
        # Log the traceback to see detailed error information
        # traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
