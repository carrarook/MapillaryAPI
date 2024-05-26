import os
import requests
import time

# Definindo a bounding box e o access token
bbox = "-49.2739352604,-25.4352817208,-49.2721489092,-25.4344235497"  # BoundingBox praça rui barbosa
access_token = "MLY|7308012082657689|f4a612db5fadbde07b652aec30c09a20"  # Client token

# Variável booleana para modo de teste
teste = True

# Criando a pasta 'Imgs' se não existir
os.makedirs("Imgs", exist_ok=True)

# Arquivo para armazenar as informações de ID, latitude e longitude
info_file_path = os.path.join("Imgs", "image_info.txt")

# URL para listar imagens
url_list_images = "https://graph.mapillary.com/images"
params_list = {
    "access_token": access_token,
    "bbox": bbox,
    "fields": "id,geometry"
}

# Iniciando o contador de tempo
start_time = time.time()

# Requisição para obter lista de imagens
response_list = requests.get(url_list_images, params=params_list)

if response_list.status_code == 200:
    data_list = response_list.json()
    if 'data' in data_list and len(data_list['data']) > 0:
        with open(info_file_path, "w") as info_file:
            # Escrevendo cabeçalho no arquivo de informações
            info_file.write("ID;Longitude;Latitude\n")

            # Conjunto para verificar IDs duplicados
            seen_ids = set()
            request_count = 0
            total_images = 0

            for item in data_list['data']:
                if teste and request_count >= 3:
                    break

                image_id = item['id']
                if image_id in seen_ids:
                    print(f"ID duplicado encontrado: {image_id}. Encerrando o programa.")
                    break

                seen_ids.add(image_id)
                coordinates = item['geometry']['coordinates']
                longitude = coordinates[0]
                latitude = coordinates[1]

                print(f"ID da Imagem: {image_id}")
                print(f"Longitude: {longitude}, Latitude: {latitude}")

                # Escrevendo as informações no arquivo
                info_file.write(f"{image_id};{longitude};{latitude}\n")

                # URL para obter a imagem
                url_image = f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=thumb_2048_url"

                # Requisição para obter a URL da imagem
                response_image = requests.get(url_image)

                if response_image.status_code == 200:
                    data_image = response_image.json()
                    image_url = data_image.get('thumb_2048_url')
                    if image_url:
                        print(f"URL da Imagem: {image_url}")

                        # Faça o download da imagem
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            # Salve a imagem localmente na pasta 'Imgs' com o nome do ID da imagem
                            image_filename = os.path.join("Imgs", f"{image_id}.jpg")
                            with open(image_filename, "wb") as file:
                                file.write(image_response.content)
                            print(f"Imagem baixada com sucesso e salva como {image_filename}")
                        else:
                            print(f"Erro ao baixar a imagem: {image_response.status_code}")
                    else:
                        print("URL da imagem não encontrada na resposta")
                else:
                    print(f"Erro na requisição da imagem: {response_image.status_code}")
                    print(response_image.text)

                request_count += 1
                total_images += 1

            # Calculando o tempo total e a média de tempo por imagem
            total_time = time.time() - start_time
            average_time_per_image = total_time / total_images if total_images > 0 else 0

            # Criando o arquivo de relatório
            report_file_path = os.path.join("Imgs", "relatorio.txt")
            with open(report_file_path, "w") as report_file:
                report_file.write(f"Bounding Box Utilizada: {bbox}\n")
                report_file.write(f"Total de Imagens: {total_images}\n")
                report_file.write(f"Tempo Total: {total_time:.2f} segundos\n")
                report_file.write(f"Média de Tempo por Imagem: {average_time_per_image:.2f} segundos\n")
                report_file.write(f"IDs Obtidos: {len(seen_ids)}\n")
                report_file.write(f"Média de IDs por Imagem: {1 if total_images == len(seen_ids) else len(seen_ids) / total_images:.2f}\n")

            print(f"Relatório salvo como {report_file_path}")

    else:
        print("Nenhuma imagem encontrada na área especificada")
else:
    print(f"Erro na requisição de listagem: {response_list.status_code}")
    print(response_list.text)
