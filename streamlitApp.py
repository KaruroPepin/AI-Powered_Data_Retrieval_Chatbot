import streamlit as st
import requests
import json
import pandas as pd

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
        except Exception as e:
            st.error(f"Exception: {e}")
else:
    st.warning('Please enter a query.')

