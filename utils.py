import json


def verificaUser(user, senha, path):
    try:
        with open(path, "rb") as file:
            json_data = file.read().decode("utf-8") # converte os bytes de volta para string

        user_data = json.loads(json_data)
        if user in user_data and user_data[user] == senha:
            return True
        else:
            print("Nome ou senha inválidos")
            return False
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
        return False
    except KeyError:
        print("Nome ou senha inválidos")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False