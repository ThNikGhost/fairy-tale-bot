import requests
import uuid
import shortuuid

def get_token(auth_token, scope='SALUTE_SPEECH_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «SALUTE_SPEECH_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return None
    
response = get_token("YjFlMjE0YjEtMjdmMi00ODQ4LWFlM2MtMmY0YmMyODVjZjI5OmYzN2YyMGNjLTc5YTQtNDZkMi1hMGNjLTMwYTRkNjg3ZWVhOA==")
if response != None:
    salute_token = response.json()['access_token']

# salute_token = """eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.sXu4N7mkIZdnR_CiszU56WRVcdRB2qo01Cui_rLRQ3BwxtND0HHtpcPv6SO6nvs9iuEJXg_knVaXvm513_ayrIC3RO5zdRMki6TwGYI8DlTmeIeL-bH3Iob9un5DmRM2hDfvRVHZ4LUUuaTNaa9OgPaw1CxrxjUqabj0eLUuabe60wI66iSZ7UWCad0EoXyrJ2Uk59bz-uy7zqxsjwzvdjMYRezz5LB-KoL0-cahU3FZ7mHa20zsFr9lI0xY2sjmHxqR_wEAgTuqAJCA0gjAhuQBq_5PQzpfWpAry-EPXLBS8rWTxUNHRmB4-Z6bJqyk4VnZ9174MKaIqnIIUU2z9g.K3xTTh5jt99ntbqaB5SffA.wo6qwgHFqRnkfwsG7EQM2jIfcntTs_vrJiuhQA2o3M5IkuDDcarpdnQZTWaf3WP4bOejkP58YGdRyEFmAqFChnL0V0NF1x1HOUecpjiesCHKqji5NosQOUHafIXoVbdz2QFG1KDTUAi1kKTerE-dnZ3SrzvP7pNdine2gBnom7a6c0BpmappGTdEmNSTgRYQvK91QfChihixSIfAyra0BxxBSbfTguyCtKU6CIxviUTWxiShdhGjQTcouANXGKcEM82UpFms0qkn4BcimFvP4ceXL3ry82hUvUd0Gk9v7TgrExQqG5EkvyC6slD_KktiEuW9lZBepIgziwk_fEv0k6wYi6nmNNwKP5vwn9LVBmpVVDtGReVXGZz6-m9Yq_J7vJfZScWAU_gnXu_q_ZgDj4XM-H1ItrpVNfjJDJTQN47bro8dghm2orabAJuVaHSEoU4nAJG2PrO1lrLIDCC5F8EIt_U0vC9kEIJfMjSITPobyp_qxv4l0qjeA_8B3Ua7IB56veiMi7eBzLe7HWzuch7cCzE5cxTDPyWAfoa1L2aRmYcX8T92R4hdfj-oC2uW6ZBnSotxqAeE6gCgEi_HUgPHxJuR86ESKgdtBmbrg2MVBThYJ8MX_BpAqnIr34JCVvsQBkpXbT1loIuehjcWnybxPrVaL2MzhbYDti1jQJKTqGCNWvp_4q84Ea2O7tfDJsjktTLgy_IZyrhjBZtyK4u5kVGeres2QosF9-vbDbk.Y0Yg8cgn_r5lr8BtpmkxedTg1MmXs-PcBnNGhoKJvQY """

def synthesize_speech(text, token=salute_token, format='wav16', voice='Tur_24000'):
    """Text to Speech

    Args:
        text (str): Текст для перевода
    """
    url = "https://smartspeech.sber.ru/rest/v1/text:synthesize"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/text"
    }
    params = {
        "format": format,
        "voice": voice
    }
    response = requests.post(url, headers=headers, params=params, data=text.encode(), verify=False)

    if response.status_code == 200:
        # Сохранение синтезированного аудио в файл
        namefile = shortuuid.uuid() + '.wav'
        with open(f'./fairy-tale/AI/voices/{namefile}', 'wb') as f:
            f.write(response.content)
    re_text = namefile
    return re_text

# print(synthesize_speech('Зайчик зайчик зайчик'))