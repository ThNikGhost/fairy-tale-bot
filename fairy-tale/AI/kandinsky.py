import json
import time
import base64
import requests
import shortuuid
from gigach2 import shorttext


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)



# if __name__ == '__main__':
def getImage(text:str):
    """Преобразует текст в картинку

    Args:
        text (str): промт для ИИ

    Returns:
        str: возвращает название под которым лежит картинка в папке с форматом изображения
    """
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '97BD02561D23C243889DB0957238BA3F', '9D80C757F9DFA8DF4511A0490CC8A21C')
    model_id = api.get_model()

    text = shorttext(text)

    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)
    
    image_base64 = images[0] # Вставьте вашу строку base64 сюда
    # Декодируем строку base64 в бинарные данные
    image_data = base64.b64decode(image_base64)
    # Открываем файл для записи бинарных данных изображения
    namefile = shortuuid.uuid()
    with open(f"./fairy-tale/AI/images/{namefile}.jpg", "wb") as file:
        file.write(image_data)

    re_text = namefile + '.jpg'
    return re_text

# [1] Жили-были в старинном лесу три веселых зайца: Барабас, Хвостик и Шустрый. Они были неразлучными друзьями и всегда веселились вместе. Однажды, прогуливаясь по лесу, они услышали странный звук. Откуда-то из-за кустов доносилось хриплое храпение. Они подошли поближе и увидели спящего волка.Какое действие хочешь предпринять?
getImage(input())
    
