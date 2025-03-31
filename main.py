from client import Client  
from server import Server 
from utils import verificaUser  


def DEBUGMODE():
    """Função para ativar/desativar modo de depuração (pula login)"""
    return False  # Retorna False para desativar modo debug


def login_request():
    """
    Solicita credenciais de login até que sejam válidas
    (exceto em modo DEBUG)
    """
    while True and not DEBUGMODE():  # Loop até login válido
        user = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")
        # Verifica credenciais no arquivo de usuários
        if verificaUser(user, senha, "users/user_data.bin"):
            break  # Sai do loop se login for válido


def main():
    """Função principal que inicia o programa"""

    print("1 - INICIAR CLIENTE\n2 - INICIAR SERVIDOR\n")
    opcao = str(input("Digite a opção desejada: "))

    while opcao != "0":  # Loop principal do menu
        if opcao == "1":  # Opção Cliente
            login_request()  # Solicita login
            main_client()  # Inicia cliente
            break
        
        elif opcao == "2":  # Opção Servidor
            ip = str(input("Digite um IP, ou 0 pro IP local: "))
            if ip == '0':
                ip = '127.0.0.1'  # IP local padrão
            
            # Cria instância do servidor
            server = Server(host=f'{ip}', port=12345)
            try:
                # Inicia o servidor
                server.start()
            except KeyboardInterrupt:
                # Encerra o servidor ao pressionar Ctrl+C
                server.stop()
            break
        else:
            print("Opção inválida")

        opcao = input("Digite a opção desejada: ")


def main_client():
    """Função principal do cliente - gerencia conexão e comunicação"""
    
    ip = str(input("Digite um IP, ou 0 pro IP local: "))
    if ip == '0':
        ip = '127.0.0.1'  # IP local padrão
    
    # Cria e conecta cliente
    client = Client(host=f'{ip}', port=12345)
    client.connect()
    
    print("Digite FIM para encerrar a conexão")
    mensagem = str(input("Digite uma mensagem: "))
    
    while True:
        # encerra o loop e desconecta
        if mensagem == "FIM" or mensagem == "fim":
            break

        # Envia mensagem para o servidor
        client.send_message(mensagem)

        # Se não for comando get/put, espera resposta
        if not (mensagem.startswith("get") or mensagem.startswith("put")):
            client.receive_message()  # Recebe resposta do servidor

        mensagem = str(input("Digite uma mensagem: "))

    # Encerra a conexão
    client.disconnect()


if __name__ == "__main__":
    """Ponto de entrada do programa - executa a função main()"""
    main()