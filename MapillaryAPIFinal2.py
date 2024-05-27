import os
import requests
import time

bbox = "-49.301704,-25.438992,-49.245699,-25.423567" # Boundig Box
access_token = "MLY|7308012082657689|f4a612db5fadbde07b652aec30c09a20" # Tolen client
teste = False # True para teste

current_dir = os.path.dirname(os.path.abspath(__file__))
imgs_dir = os.path.join(current_dir, "Imgs")
os.makedirs(imgs_dir, exist_ok=True)
info_file_path = os.path.join(imgs_dir, "image_info.txt")

url_list_images = "https://graph.mapillary.com/images"
params_list = {
    "access_token": access_token,
    "bbox": bbox,
    "fields": "id,geometry"
}

start_time = time.time() # pro relatorio (deve ter um jeito de medir pelos ms de cada req)

response_list = requests.get(url_list_images, params=params_list)

if response_list.status_code == 200:
    data_list = response_list.json()
    if 'data' in data_list and len(data_list['data']) > 0:
        with open(info_file_path, "w") as info_file:
            info_file.write("ID;Longitude;Latitude\n")

            seen_ids = set()
            request_count = 0
            total_images = 0

            for item in data_list['data']:
                if teste and request_count >= 50: # define quantas req vou fazer no teste
                    break

                image_id = item['id']
                if image_id in seen_ids:
                    print(f"ID duplicado encontrado: {image_id}. Encerrando o programa.")
                    break

                seen_ids.add(image_id)
                coordinates = item['geometry']['coordinates']
                longitude = coordinates[0]
                latitude = coordinates[1]

                longitude_str = f"{longitude:.8f}" #organiza pra todos os dados terem o mesmo "tamanho"
                latitude_str = f"{latitude:.8f}"   #organiza pra todos os dados terem o mesmo "tamanho"

                print(f"ID da Imagem: {image_id}")
                print(f"Longitude: {longitude_str}, Latitude: {latitude_str}")

                info_file.write(f"{image_id};{longitude_str};{latitude_str}\n")

                url_image = f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=thumb_2048_url"

                response_image = requests.get(url_image)

                if response_image.status_code == 200:
                    data_image = response_image.json()
                    image_url = data_image.get('thumb_2048_url')
                    if image_url:
                        print(f"URL da Imagem: {image_url}")

                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_filename = os.path.join(imgs_dir, f"{image_id}.jpg")
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

            total_time = time.time() - start_time
            average_time_per_image = total_time / total_images if total_images > 0 else 0

            report_file_path = os.path.join(imgs_dir, "relatorio.txt")
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
