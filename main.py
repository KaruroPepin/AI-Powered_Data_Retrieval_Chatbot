from client_initialization import client
from BotContext import QueryMaker
from data import data


def initialize_bot(prompt_usuario):

    dbschema = data()
    messages=QueryMaker(prompt_usuario, client, dbschema)
    print(messages)

###########################################################################################

def main():
    while True:
        prompt_usuario = input("Ingrese su consulta o escriba 'salir' para terminar: ")
        if prompt_usuario.lower() == 'salir':
            break
        initialize_bot(prompt_usuario)

if __name__ == "__main__":
    main()