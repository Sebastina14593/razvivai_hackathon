import requests
import json
def get_chat_adhoc(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.

    Возвращает:
    - str: Ответ от API в виде текстовой строки.

    """

    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 1,
        # Генерация температуры (насколько случайным будет ответ при генерации ответа. Если 0, то будет выбираться самый надежный результат (всегда один и тот же ответ))
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов (также за разнообразие)
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,
        # Потоквая ли передача ответов (отправляется ли каждый токен в ответ пользователю или сразу весь ответ)
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения (можно ставить побольше, чтобы не повторялись в больших текстах)
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    try:
        # response = requests.post("POST", url, headers=headers, data=payload, verify=False)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1