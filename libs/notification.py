import requests
from common.settings import DISCORD_BOT_TOKEN


def send_discord_message(uid: int, message: str) -> None:
    http_headers = { 'Authorization': f'Bot {DISCORD_BOT_TOKEN}', 'Content-Type': 'application/json' }
    res = requests.post(
        url='https://discord.com/api/v9/users/@me/channels',
        headers=http_headers,
        json={ "recipient_id": str(uid) }
    )

    if res.status_code == 200:
        dm_channel = res.json()
        channel_id = dm_channel['id']

        requests.post(
            url=f'https://discord.com/api/v9/channels/{channel_id}/messages',
            headers=http_headers,
            json={ 'content': message }
        )