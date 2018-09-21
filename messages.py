from configparser import ConfigParser
import json
import logging
import sys

from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser

logging.basicConfig(level=logging.WARNING)


class Message:
    def __init__(self, msg):
        self.outgoing = msg.out
        self.private = isinstance(msg.to_id, PeerUser)

        if isinstance(msg.to_id, PeerUser):
            self.to_id = msg.to_id.user_id
        elif isinstance(msg.to_id, PeerChat):
            self.to_id = msg.to_id.chat_id
        elif isinstance(msg.to_id, PeerChannel):
            self.to_id = msg.to_id.channel_id
        else:
            raise RuntimeError('invalid peer: ', self.to_id)

        if self.private:
            self.chat = self.to_id if self.outgoing else self.from_id
        else:
            self.chat = self.to_id

        self.from_id = msg.from_id
        self.timestamp = msg.date.isoformat()
        self.text = msg.message.message
        self.media = type(msg.media).__name__ if msg.media is not None else ""

        self.id = msg.id

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('telegram.ini')

    api_id = config['api']['id']
    api_hash = config['api']['hash']

    phone = config['user']['phone']
    password = config['user']['password']
    session = config['user']['session']

    client = TelegramClient(session, api_id, api_hash)
    client.start(phone, password)


    @client.on(events.NewMessage)
    async def _(e):
        print(e, file=sys.stderr)
        print(Message(e).to_json())


    client.run_until_disconnected()
