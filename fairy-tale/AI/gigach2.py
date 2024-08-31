"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials="OTg5ZWE3MzMtN2IyNS00ZGYyLWI3OTEtZWE4ZjQ0M2E2MzZmOjFjNzJkNzc5LWNkZjUtNGQyMi04Zjc0LTQ4Y2I2N2RjOTYxZA==", verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="""Напиши как бы выглядела иллюстрация к этому тексту, кратко. не более 20 слов."""
    )
]
# Начало перед историей нету
# Выжимка на английском
# Он не воспринимает слова
# Он не заканчивает сказку

def shorttext(user_input):
    messages.append(HumanMessage(content="Пожалуйста, перефразируй следующий текст: "+user_input))
    res = chat.invoke(messages)
    messages.append(res)
    print(res.content)
    return res.content


