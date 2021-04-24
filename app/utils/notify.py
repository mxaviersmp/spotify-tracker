import os
from typing import Dict, Optional, Text

import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def get_chats(token: Optional[Text] = None) -> Dict[int, Text]:
    """
    Gets all active chats with telegram bot.

    Parameters
    ----------
    token : str, optional
        telegram bot token, by default TELEGRAM_TOKEN

    Returns
    -------
    dict
        dictionary with chat id and user name
    """
    if token is None:
        token = TELEGRAM_TOKEN
    response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(token))
    resp_json = response.json()
    messages = resp_json.get('result')

    chats = {}
    for data in messages:
        chat = data.get('message').get('chat')
        chat_id = chat.get('id')
        chats[chat_id] = '{} {} (@{})'.format(
            chat.get('first_name'),
            chat.get('last_name'),
            chat.get('username')
        )
    return chats


def send(
    msg: Text, token: Optional[Text] = None, chat_id: Optional[int] = None
) -> Dict:
    """
    Sends a message to the chat.

    Parameters
    ----------
    msg : str
        message to send
    token : str, optional
        telegram bot token, by default TELEGRAM_TOKEN
    chat_id : int, optional
        telegram chat, by default TELEGRAM_CHAT_ID

    Returns
    -------
    dict
        post result
    """
    if token is None:
        token = TELEGRAM_TOKEN
    if chat_id is None:
        chat_id = int(TELEGRAM_CHAT_ID)
    data = {'chat_id': chat_id, 'text': msg}
    respose = requests.post(
        'https://api.telegram.org/bot{}/sendMessage'.format(token),
        json=data
    )
    resp_json = respose.json()
    return resp_json.get('result')
