import pandas as pd
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from io import BytesIO
import pdfplumber

# SharePoint site URL and file path
site_url = "https://evopointsolutions.sharepoint.com/sites/AI_POC_SPACE"
file_url = "/sites/AI_POC_SPACE/Shared Documents/Fundamentos de inteligencia de negocio_Mo¿dulo2_Disen¿o de un data warehouse.pdf"


# Authentication details
username = "cpepin@evopointsolution.com"
password = "Preaching7-Ending-Walk"

# Authenticate and create client context
ctx_auth = AuthenticationContext(site_url)
if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(site_url, ctx_auth)
    response = File.open_binary(ctx, file_url)
    
    # Convert response content to BytesIO for pdfplumber
    pdf_file = BytesIO(response.content)
    
    # Extract text from PDF
    with pdfplumber.open(pdf_file) as pdf:
        # Assuming the text is in the first page; modify as needed
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Convert text to pandas DataFrame (depends on text format)
        # This is a basic example; parsing will depend on your PDF structure
        data = [line.split() for line in text.split('\n') if line]
        df = pd.DataFrame(data)
        print(df.head())
else:
    print("Authentication failed.")