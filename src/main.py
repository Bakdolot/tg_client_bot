import os
from flask import Flask, request
from bot import bot
import telebot
import requests
from config import SERVER_DOMAIN_OR_IP, BOT_TOKEN, SERVER_PORT, SERVER_HOST


server = Flask(__name__)


@server.route("/", methods=["POST"])
def receive_update():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return {'ok':True}


def set_webhook(domain, token):
    response = requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={domain}').json()
    if not response['ok']:
        raise ValueError(response)
    print(response)



if __name__ == "__main__":
    set_webhook(SERVER_DOMAIN_OR_IP, BOT_TOKEN)
    server.run(host=SERVER_HOST, port=SERVER_PORT)
