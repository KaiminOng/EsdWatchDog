import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

@app.route("/send_message/<bot_chatID>", methods=['POST'])
def telegram_bot_sendtext(bot_chatID):
    
    bot_token = '1129690128:AAFzGAL-Rur8QAZyjG2_62f5tvQvOKjv29w'
    # bot_chatID = '-1001260714304'
    bot_message = "TESTING EH"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

test = telegram_bot_sendtext("-393119922")
print(test)