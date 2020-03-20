from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Not sure the configurations, Need updates
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/watchlist'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
CORS(app)

# class Watchlist(db.Model):
#     __tablename__ = 'watchlist'

#     # Double check with DB
#     userid = db.Column(db.String(13), primary_key=True)
#     endpoint = db.Column(db.String(64), nullable=False)
#     chatid = db.Column(db.String(64), nullable=False)
    

#     def __init__(self, userid, endpoint, chatid):
#         self.userid = userid
#         self.endpoint = endpoint
#         self.chatid = chatid

#     def json(self):
#         return {"userid": self.userid, "endpoint": self.endpoint, "chatid": self.chatid}

# TO GET ALLL USERIDS + ENDPOINTS (Not sure if necessary, but leaving it for now)
# @app.route("/watchlist")
# def get_all():
# 	return jsonify({"lists": [watchlist.json() for watchlist in Watchlist.query.all()]})

@app.route("/watchlist/<string:userid>")
def find_by_userid(userid):
    return jsonify({"message": "Find By User('{}') Here".format(userid)},200)
    # watchlist = Watchlist.query.filter_by(userid=userid).first()
    # if watchlist:
    #     return jsonify(watchlist.json())
    # return jsonify({"message": "Watchlist not found."}, 404)
    


@app.route("/watchlist", methods=['POST'])
def create_endpoint():

    data = request.get_json()
    userid = data["userid"]
    chat = data["chat"]
    endpoint = data["endpoint"]

    return jsonify({"message": "CREATE ENDPOINT W '{}', '{}', '{}' HERE".format(userid, chat, endpoint)}, 200)

    # userid = request.args.get('userid', None)
    # chat = request.args.get('chat', None)               # In the format of Chat Name 
    # endpoint = request.args.get('endpoint', None)

    # Codes to Get ChatID of Chat that is monitoring the endpoint
    # ...
    # chatid = ...
    # ...

    # if (Watchlist.query.filter_by(userid=userid, chatid=chatid, endpoint=endpoint).first()):
    #     return jsonify({"message": "This endpoint already exists in the chat '{}'.".format(chat)}, 400)

    
    # newEndpoint = Watchlist(userid, endpoint, chatid)

    # try:
    #     db.session.add(newEndpoint)
    #     db.session.commit()
    # except:
    #     return jsonify({"message": "An error occurred creating the endpoint."}, 500)

    # return jsonify(newEndpoint.json(), 201)
    


if __name__ == '__main__':
    app.run(host="esdwatchdog.com", port=5001, debug=True)