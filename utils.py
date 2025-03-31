import json

def verificaUser(user, senha, path):
    try:
        # Abre o arquivo em modo binário para evitar problemas de codificação
        with open(path, "rb") as file:
            # Lê o conteúdo do arquivo e decodifica de bytes para string UTF-8
            json_data = file.read().decode("utf-8")

        # Converte a string JSON em um dicionário Python
        user_data = json.loads(json_data)
        
        # Verifica se o usuário existe e se a senha corresponde
        if user in user_data and user_data[user] == senha:
            return True  # Credenciais válidas
        else:
            print("Nome ou senha inválidos")
            return False  # Credenciais inválidas
            
    except json.JSONDecodeError:
        # Erro se o arquivo não contiver um JSON válido
        print("Erro ao decodificar o arquivo JSON.")
        return False
        
    except KeyError:
        # Erro se a chave (usuário) não existir no dicionário
        print("Nome ou senha inválidos")
        return False
        
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Ocorreu um erro inesperado: {e}")
        return False