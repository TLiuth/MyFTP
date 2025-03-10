from client import Client
from server import Server

def main():

    opcao = str(input("Digite a opção desejada: "))



    while opcao != "0":
        if opcao == "1":
            main_client()

            break
        elif opcao == "2":
            server = Server(host='127.0.0.1', port=12345)
            try:
                # Inicia o servidor
                server.start()
            except KeyboardInterrupt:
                # Encerra o servidor ao pressionar Ctrl+C
                server.stop()
        else:
            print("Opção inválida")

        opcao = input("Digite a opção desejada: ")

# trata do fluxo principal do cliente
def main_client():
    client = Client(host='127.0.0.1', port=12345)
    client.connect()
    print("Digite FIM para encerrar a conexão")
    mensagem = str(input("Digite uma mensagem: "))
    while mensagem != "FIM":

        # encerra o loop e desconecta
        if mensagem == "FIM":

            break

        # demais comandos serão processados no server por meio do envio de mensagem
        # Envia uma mensagem
        client.send_message(mensagem)

        # Recebe uma resposta
        client.receive_message()

        mensagem = str(input("Digite uma mensagem: "))

    # Encerra a conexão
    client.disconnect()

# trata do fluxo principal do server
def main_server():
    return

if __name__ == "__main__":
    main()