import json


def verificaUser(user, senha):
    with open("users/user_data.bin", "rb") as file:
        json_data = file.read().decode("utf-8") # converte os bytes de volta para string

    user_data = json.loads(json_data)
    try:
        if(user_data[user] == senha):
            return True
        print("Nome ou senha inválidos")
        return False
    except:
        print("Nome ou senha inválidos")
        return False