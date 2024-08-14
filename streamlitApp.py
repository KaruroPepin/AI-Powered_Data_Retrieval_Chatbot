import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt



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
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'query': query})
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

                    funciones_graficos = {
                        "barras": lambda df, ax: df.plot(kind='bar', ax=ax),
                        "lineas": lambda df, ax: df.plot(kind='line', ax=ax),
                        "circular": lambda df, ax: df.set_index(df.columns[0]).plot(kind='pie', y=df.columns[1], ax=ax),
                        "dispersion": lambda df, ax: df.plot(kind='scatter', x=df.columns[0], y=df.columns[1], ax=ax),
                        "histograma": lambda df, ax: df.plot(kind='hist', y=df.columns[1], ax=ax),
                        "area": lambda df, ax: df.plot(kind='area', ax=ax),
                        "radar": None  # Gráficos personalizados como radar podrían necesitar funciones adicionales
                    }
                    
                    funcion_grafico = funciones_graficos.get(response_chart)

                    if funcion_grafico:
                        st.header(response_title)
                        # Crear la figura y eje de Matplotlib
                        fig, ax = plt.subplots()
                        
                        # Call the plotting function with the DataFrame and the axis
                        funcion_grafico(df, ax)

                        # Display the plot in Streamlit
                        st.pyplot(fig)
                    else:
                        st.warning("Tipo de gráfico no reconocido.")
                else:
                    st.warning("No data returned.")


        except Exception as e:
            st.error(f"Exception: {e}")
else:
    st.warning('Please enter a query.')

