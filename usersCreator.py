import json

# Dicionário com usuário e senha
user_data = {
    "admin": "123",
    "user1": "321",
    "user2": "000"
}

# Converte o dicionário para JSON
json_data = json.dumps(user_data)

# Salva o JSON em um arquivo binário
with open("user_data.bin", "wb") as file:
    file.write(json_data.encode('utf-8'))  # Converte a string JSON em bytes e salva

print("Dicionário salvo em 'user_data.bin'.")