import streamlit as st
import requests
from requests.exceptions import RequestException
import json
import pandas as pd
import matplotlib.pyplot as plt

from GraphicFunctions import *

# Streamlit app title
st.title('Test Flask API with Streamlit')

# Input for user query
query = st.text_input('Enter your query:', '')

# Button to send the request
if st.button('Send'):
    if query:
        try:
            # Send POST request to the Flask API
            response = requests.post(
                'http://127.0.0.1:5000/ask',
                headers={
                    'Content-Type': 'application/json',
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept-Encoding": "*",
                    "Connection": "keep-alive"},
                data=json.dumps({'query': query}),
                timeout=(10, 30)  # (connection timeout, read timeout)
            )
            
            # Check if the request was successful
            if response.status_code == 200:

                # Parse the JSON response
                response_json = response.json()
                
                if response_json['classification'] == 'Base de Datos':
                    # Extract the final_query and data
                    response_query = response_json.get('final_query')
                    response_data = response_json.get('data')

                    # Display the SQL statement
                    st.header("Sentencia SQL:")
                    st.success(response_query)

                    ## Display the dataset as a dataframe if available
                    if response_data:
                        # Assuming response_data is in a format convertible to a dataframe
                        df = pd.DataFrame(response_data)
                        st.header("Dataset:")
                        st.dataframe(df)
                    else:
                        st.warning("No data returned.")
                
                elif response_json['classification'] == 'Documento':
                    response_doc_response = response_json.get('respuesta')

                    # Display the SQL statement
                    st.header("Respuesta:")
                    st.success(response_doc_response)

                elif response_json['classification'] == 'Grafico':
                    response_chart = response_json.get('chart_type')
                    response_data = response_json.get('chart_data')
                    response_title = response_json.get('chart_title')

                    # Assuming response_data is in a format convertible to a dataframe
                    df = pd.DataFrame(response_data)

                    # Convert columns to numeric if possible
                    df = df.apply(pd.to_numeric, errors='coerce')

                    # Dicionario de funciones lambda
                    funciones_graficos = {
                        "barras": plot_barras,
                        "lineas": plot_lineas,
                        "circular": plot_circular,
                        "dispersion": plot_dispersión,
                        "histograma": plot_histograma,
                        "area": plot_area,
                        "radar": None  
                    }

                    funcion_grafico = funciones_graficos.get(response_chart)

                    if funcion_grafico:
                        st.header(response_title)
                        # Crear la figura y eje de Matplotlib
                        fig, ax = plt.subplots()

                        # Verifica que el DataFrame no esté vacío y tenga datos numéricos
                        if not df.empty and not df.select_dtypes(include=['number']).empty:

                            # Llamar a la función con el DataFrame y el eje
                            funcion_grafico(df, ax)
                            
                            # Display Streamlit
                            st.pyplot(fig)
                        else:
                            st.error("No hay datos numéricos para graficar.")
                    else:
                        st.warning("Tipo de gráfico no reconocido.")
                else:
                    st.error("No data returned.")               

        except RequestException as e:
            st.error(f"RequestException: {e}")

        except Exception as e:
            st.error(f"Exception: {e}")
else:
    st.warning('Please enter a query.')

