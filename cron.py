import json
import smtplib
import secrets
from imbox import Imbox

config = {}

try:
    with open("config.json", "r") as configF:
        config = json.load(configF)
except FileNotFoundError:
    with open("config.json", "w") as configF:
        config = {"username": "", "password": "", "server": ""}
        print(json.dumps(config), file=configF)
        quit(0)

with smtplib.SMTP_SSL(config['server'] + ':465') as server_out:
    server_out.login(config['username'], config['password'])
    with Imbox(config['server'],
               username=config['username'],
               password=config['password'],
               ssl=True) as inbox:
        inbox_messages = inbox.messages()
        for uid, messageIn in inbox_messages:
            password = secrets.token_urlsafe(16)
            text = "We created a password for you! Its very secure, but we do not recommend to use it. \n Here it is\n" + password
            message = 'From: Passwords (not) very secure <' + config['username'] + '>\nSubject: {}\n\n{}'.format("Your new Password", text)
            server_out.sendmail(config['username'], messageIn.sent_from[0]['email'], message)
            inbox.delete(uid)


