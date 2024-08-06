from client_initialization import client
from BotContext import QueryMaker
from data import data


def initialize_bot(prompt_usuario):

    dbschema = data()
    messages=QueryMaker(prompt_usuario, client, dbschema)
    print(messages)