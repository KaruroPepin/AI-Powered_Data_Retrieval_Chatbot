import os
from dotenv import load_dotenv
import pandas as pd

#Azure and local Connection
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
import pyodbc

#Directory Connetion
from PyPDF2 import PdfReader
import docx2txt
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

def az_connetion():
    load_dotenv()
    server = os.environ['SQL_DATABASE_SERVER']
    database = os.environ['SQL_DATABASE_NAME']
    username = os.environ['SQL_DATABASE_USERNAME']
    password = os.environ['SQL_DATABASE_PASSWORD']
    driver = os.environ['SQL_DATABASE_DRIVER']
    if driver.startswith('{') and driver.endswith('}'):
        driver = driver[1:-1]  # Remove the curly braces for SQLAlchemy
        
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    return conn_str

def az_schema():
    conn_str = az_connetion()
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

    try:
        engine = create_engine(connection_url)
        # print("Engine creation successful!")

        with engine.connect() as connection:
            # print("Connection successful!")
            
            # Initialize MetaData object
            metadata = MetaData()

            # Reflect the database schema
            metadata.reflect(bind=engine)

            # Extract metadata for a specific table or all tables
            inspector = inspect(engine)

            # Iterate through each schema and list all tables and their columns
            # schemas = inspector.get_schema_names()

            # Specific schemas
            schemas = ['SalesLT']
            

        # string
            metadata_str = f"Database: {engine.url.database}\n"
            for schema in schemas:
                tables = inspector.get_table_names(schema=schema)
                metadata_str += f"Schema: {schema}\n"
                for table in tables:
                    columns = inspector.get_columns(table, schema=schema)
                    metadata_str += f"  Table: {table}\n"
                    for column in columns:
                        column_name = column['name']
                        column_type = str(column['type'])  # Convert column type to string for readability
                        metadata_str += f"    Column: {column_name}, Type: {column_type}\n"

            #Return the metadata
            return metadata_str

    except SQLAlchemyError as e:
        print(f"An error occurred while creating the engine: {e}")
 
def az_data(query):
        
    conn_str = az_connetion()
    
    #Getting actual data
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(query, conn)

    return df

#-----------

def local_connetion():
    username = os.environ['LOCAL_USERNAME']
    password = os.environ['LOCAL_USER_PASSWORD']
    host = os.environ['LOCALHOST']
    port = os.environ['LOCAL_PORT']
    database = os.environ['LOCAL_DATABASE_NAME']
    url = LOCAL_URL = 'mssql+pyodbc://{user}:{passwd}@{host}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server'.format(user=username, passwd=password, host=host, port=port, db=database)

    return url

def local_data(query):
        
    url = local_connetion()
    engine = create_engine(url)
    df = pd.read_sql(query, engine)

    return df

def local_schema():
    connection_url = local_connetion()

    try:
        engine = create_engine(connection_url)
        # print("Engine creation successful!")

        with engine.connect() as connection:
            # print("Connection successful!")
            
            # Initialize MetaData object
            metadata = MetaData()

            # Reflect the database schema
            metadata.reflect(bind=engine)

            # Extract metadata for a specific table or all tables
            inspector = inspect(engine)

            # Iterate through each schema and list all tables and their columns
            # schemas = inspector.get_schema_names()

            # Specific schemas
            schemas = ['dbo']
            

        # string
            metadata_str = f"Database: {engine.url.database}\n"
            for schema in schemas:
                tables = inspector.get_table_names(schema=schema)
                metadata_str += f"Schema: {schema}\n"
                for table in tables:
                    columns = inspector.get_columns(table, schema=schema)
                    metadata_str += f"  Table: {table}\n"
                    for column in columns:
                        column_name = column['name']
                        column_type = str(column['type'])  # Convert column type to string for readability
                        metadata_str += f"    Column: {column_name}, Type: {column_type}\n"

            #Return the metadata
            return metadata_str

    except SQLAlchemyError as e:
        print(f"An error occurred while creating the engine: {e}")

#-----------

def read_documents(prompt_usuario, client):
    load_dotenv()

    #Directorio
    directory = os.environ['DIRECTORY']

    text = ""
    files = os.listdir(directory)
    
    for file in files:
        file_path = os.path.join(directory, file)
        extension = file.split('.')[-1].lower()

        if extension == 'pdf':
            # Read PDF file
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        elif extension == 'docx':
            # Read DOCX file
            text += docx2txt.process(file_path)
        
        elif extension == 'txt':
            # Read TXT file
            with open(file_path, 'r', encoding='utf-8') as f:
                text += f.read()
        
        else:
            print(f"Unsupported file type: {extension}")
    
    #2. Crear los Chuncks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    #3. Crear Embedding
    # api_key = os.environ['AZURE_OPENAI_API_KEY'] #Pass your key here
    api_key = os.environ['OPENAI_API_KEY']

    embeddings = OpenAIEmbeddings(openai_api_key = api_key)

    #4. Crear Vector Store
    vector_store = FAISS.from_texts(chunks, embeddings)

    #5. Obtener Similitudes
    match = vector_store.similarity_search(prompt_usuario)

    #Enviar Respuesta
    chain = load_qa_chain(client, chain_type="stuff")
    response = chain.run(input_documents = match, question = prompt_usuario)

    return response