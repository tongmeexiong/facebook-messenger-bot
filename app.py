import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__)

#  Get access tokens from .env file
app.config['ACCESS_TOKEN'] = os.getenv('ACCESS_TOKEN')
app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')

ACCESS_TOKEN = 'ACCESS_TOKEN'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this route
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:

        # get  message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if matched, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["Hello! how can I help you?", "This Week I am busy with Prime! Sorry I have no available times to book at shoot."]
    # return selected item to the user
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
