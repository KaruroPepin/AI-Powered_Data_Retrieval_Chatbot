import streamlit as st
import requests
import json

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
                response_data = response.json()
                st.success(f"Response: {response_data.get('response', 'No response key found')}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Exception: {e}")
    else:
        st.warning('Please enter a query.')

