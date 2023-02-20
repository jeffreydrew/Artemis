import openai
import random
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def handle_responses(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message that you can modify`"

    if p_message == "bye":
        return "See you later!"

    if p_message[0] == '/':
        response = openai.Completion.create(
            model="text-babbage-001",
            prompt=p_message[1:],
            temperature=0.7,
            max_tokens=150,
            top_p=0.5,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        return response['choices'][0]['text']
