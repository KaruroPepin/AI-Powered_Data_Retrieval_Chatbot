from client_initialization import client
from BotContext import *
from data import *


def database_search(prompt_usuario):

    dbschema = local_schema()
    final_query = QueryMaker(prompt_usuario, client, dbschema)
    data = local_data(final_query)

    return final_query, data

def document_search(prompt_usuario):

    doc_response = read_documents(prompt_usuario, client)

    return doc_response