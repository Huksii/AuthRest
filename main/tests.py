import requests


def get_token(username, password, token_url):
    
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(token_url, data=data)
    
    return response.json().get("token")


def get_list():
    token_url = "http://127.0.0.1:8080/api/api-token-auth/"
    
    username = 'a'
    password = '1'
    
    token = get_token(username, password, token_url)
    
    if token:
        headers = {
            "Authorization": f"Token {token}"
        }
        
        data = {
            "name": "string"
        }
        import string, random
        
        while True:
            if len(data["name"]) == 10:
                requests.post("http://127.0.0.1:8080/api/categories/",
                    data=data, headers=headers)
                print("Запрос отправлен")
                data["name"] = ""
            else:
                data["name"] += random.choice(" ".join(string.ascii_letters).split())
                
    else:
        print("Error Authorization")




get_list()

