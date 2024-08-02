# import os
# import pandas as pd
# from io import BytesIO
# from source_service_client import get_service_client_account_key
# from langchain.output_parsers import PandasDataFrameOutputParser

# def data():
    
#     #Connection to Storage Account
#     account_name = os.environ['ACCOUNT_NAME']
#     account_key = os.environ['ACCOUNT_KEY']
#     file_system_name = os.environ['FYLE_SYSTEM_NAME']
#     service_client = get_service_client_account_key(account_name=account_name, account_key=account_key)
#     file_system_client = service_client.get_file_system_client(file_system_name)
#     paths = file_system_client.get_paths()


#     for path in paths:
#         # Check if the path is a file (you may want to skip directories)
#         if not path.is_directory:
#             file_client = file_system_client.get_file_client(path.name)
            
#             # Download the file's content
#             try:
#                 downloaded_bytes = file_client.download_file().readall()

#                 # Reading the files
#                 try:
#                     df = pd.read_excel(BytesIO(downloaded_bytes))
#                     print(f"Data from {path.name}:")
#                     # print(df.head(10))

#                 except Exception as e:
#                     print(f"Could not read {path.name} as an Excel file: {e}")

#             except Exception as e:
#                 print(f"An error occurred while accessing {path.name}: {e}")
    
#     # parser = PandasDataFrameOutputParser()
#     df_dict = df.to_dict(orient='records')
#     return df_dict

# # d = data()
# # print(type(d))

###################################################################################################################
# import os
# import pyodbc
# from dotenv import load_dotenv

# load_dotenv()

# server = os.environ['SQL_DATABASE_SERVER']
# database = os.environ['SQL_DATABASE_NAME']
# username = os.environ['SQL_DATABASE_USERNAME']
# password = os.environ['SQL_DATABASE_PASSWORD']
# driver = os.environ['SQL_DATABASE_DRIVER']

# connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# conn = pyodbc.connect(connectionString)

# SQL_QUERY = """
# SELECT TOP 3 name, collation_name FROM sys.databases
# """
# cursor = conn.cursor()
# cursor.execute(SQL_QUERY)
# row = cursor.fetchone()
# while row:
#     print (str(row[0]) + " " + str(row[1]))
#     row = cursor.fetchone()


###################################################################################################################
import os
from dotenv import load_dotenv

#Connection
import json 
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


def data():
    load_dotenv()
    server = os.environ['SQL_DATABASE_SERVER']
    database = os.environ['SQL_DATABASE_NAME']
    username = os.environ['SQL_DATABASE_USERNAME']
    password = os.environ['SQL_DATABASE_PASSWORD']
    driver = os.environ['SQL_DATABASE_DRIVER']
    if driver.startswith('{') and driver.endswith('}'):
        driver = driver[1:-1]  # Remove the curly braces for SQLAlchemy
        

    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
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
            metadata_str = ""
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

            return metadata_str

    except SQLAlchemyError as e:
        print(f"An error occurred while creating the engine: {e}")
