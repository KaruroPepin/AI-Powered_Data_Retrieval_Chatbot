import os
from dotenv import load_dotenv
import pandas as pd

#local Connection
import sqlite3

#Azure Connection
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
import pyodbc

#pydataset 
from pydataset import data

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
    _df = pd.read_sql(query, conn)

    df = {
        'id': 'azure_dataset',
        'data': _df
    }

    return df

#-----------

def local_connetion():
    username='sa'
    password='r75N0VWhrptkpJ8rXHX8r4R5SUSlgzht1zpITKAd4ww='
    host='DESKTOP-G5JDHH1'
    port='1433'
    database= 'bpd_gestionbienesReportesV2'
    url = 'mssql+pyodbc://{user}:{passwd}@{host}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server'.format(user=username, passwd=password, host=host, port=port, db=database)

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

def local_schema_pd():
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

            metadata_list = []
            for schema in schemas:
                tables = inspector.get_table_names(schema=schema)
                for table in tables:
                    columns = inspector.get_columns(table, schema=schema)
                    for column in columns:
                        column_name = column['name']
                        column_type = str(column['type'])  # Convert column type to string for readability
                        metadata_list.append({
                            'schema': schema,
                            'table': table,
                            'column': column_name,
                            'type': column_type
                        })

    # Convert the list of dictionaries to a pandas DataFrame
            metadata_df = pd.DataFrame(metadata_list)
        return metadata_df

    except SQLAlchemyError as e:
        print(f"An error occurred while creating the engine: {e}")

#-----------

def SakilaRentalStore_connetion():
    username='sa'
    password='r75N0VWhrptkpJ8rXHX8r4R5SUSlgzht1zpITKAd4ww='
    host='DESKTOP-G5JDHH1'
    port='1433'
    database= 'SakilaRentalStore'
    url = 'mssql+pyodbc://{user}:{passwd}@{host}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server'.format(user=username, passwd=password, host=host, port=port, db=database)

    return url

def SakilaRentalStore_schema():
    connection_url = SakilaRentalStore_connetion()

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

def merge_metadata_strings():
    # Call the two functions and merge their outputs
    metadata_str_1 = SakilaRentalStore_schema()
    metadata_str_2 = local_schema()
    merged_metadata_str = metadata_str_1 + "\n" + metadata_str_2
    return merged_metadata_str

# print(type(local_schema_pd().to_string()))






