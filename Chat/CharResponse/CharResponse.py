from Bot.models import Bot, BotCharacter, BotMessages
from Chat.models import Chat, ChatMessage
import requests
import json

proxy_url = ""


class CharResponse:
    def __init__(self, method: str, bot: Bot, bot_character: BotCharacter, chat_messages: [ChatMessage], bot_messages: [BotMessages]):
        self.method = method
        self.bot = bot
        self.bot_character = bot_character
        self.chat_messages = chat_messages
        self.bot_messages = bot_messages

    def get_response(self) -> str:

        def format_message(bot_message) -> dict:
            if bot_message.rol:
                rol = "user"
            else:
                rol = "char"

            return {
                "rol": rol,
                "content": bot_message.content
            }

        messages = list(
            map(
                lambda x: format_message(x),
                self.bot_messages
            )
        )

        messages += list(
            map(
                lambda x: format_message(x),
                self.chat_messages
            )
        )

        options = {
            "model": "gpt-3.5-turbo-16k",
            "messages": messages,
            "temperature": self.bot_character.temperature,
            "max_tokens": self.bot_character.max_tokens,
            "presence_penalty": self.bot_character.presence_penalty,
            "frequency_penalty": self.bot_character.frequency_penalty,
            "stream": self.bot_character.stream
        }
        response = requests.post(
            url=proxy_url + "chat/completions",
            headers={
                "Authorization": "Bearer {token}",
                "Content-Type": "application/json"
            },
            data=json.dumps(options)
        )
        return response.text