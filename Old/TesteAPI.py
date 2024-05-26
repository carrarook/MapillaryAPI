import requests


bbox = "-49.2739352604,-25.4352817208,-49.2721489092,-25.4344235497" # BoundingBox praça rui barbosa
access_token = "MLY|7308012082657689|f4a612db5fadbde07b652aec30c09a20"  # Client token


urlId = f"https://graph.mapillary.com/images?bbox={bbox}&access_token={access_token}"

response = requests.get(urlId)

# GPT
if response.status_code == 200:  
    # Parse a resposta JSON
    data = response.json() 
    # Faça algo com os dados recebidos
    print(data)
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)


fields = "793764837914630" # Id


urlImgs = "https://graph.mapillary.com/images" 
params = {
    "access_token": access_token,
    "fields": fields,
    "bbox": bbox 
}


response = requests.get(urlImgs, params=params)

# GPT
if response.status_code == 200:
    data = response.json()
    image_id = data['data'][0]['id']
    print(f"ID da Imagem: {image_id}")
    
    # URL para obter a imagem
    image_url = f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=thumb_2048_url"
    
    # Faça a requisição GET para obter a URL da imagem
    response = requests.get(image_url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['thumb_2048_url']
        print(f"URL da Imagem: {image_url}")
        
        # Faça o download da imagem
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Salve a imagem localmente
            with open("imagem.jpg", "wb") as file:
                file.write(image_response.content)
            print("Imagem baixada com sucesso e salva como imagem.jpg")
        else:
            print(f"Erro ao baixar a imagem: {image_response.status_code}")
    else:
        print(f"Erro na requisição da imagem: {response.status_code}")
        print(response.text)
else:
    print(f"Erro na requisição de listagem: {response.status_code}")
    print(response.text)