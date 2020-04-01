from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from validator import validate_request
import requests as r
import os

# Start flask app
app = Flask(__name__)
CORS(app)

os.environ['DH_URI'] = 'http://esdwatchdog.com:5000'
dataHandler_host = os.environ.get('DH_URI')

@app.route('/watchlist/get/<string:account_id>', methods=['GET'])
def get_account_watchlist(account_id):

    # Formulate request
    api_route = '/endpoint/get'

    request_data = {'account_id' : account_id}
    response = r.get(f"{dataHandler_host}{api_route}", json=request_data, timeout=10.0)

    try:
        response.raise_for_status()
    except Exception:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when retrieving watchlist'}), 500)

    # Successful response
    return make_response(jsonify(response.json()), 200)



@app.route('/watchlist/new', methods=['POST'])
def add_new_endpoint():

    # Specify the required fields to be present in the request
    required_fields = ['id', 'endpoint', 'chat_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Formulate request
    api_route = '/endpoint/new'

    for contact in request.json['chat_id']:
        request_data = {'account_id' : request.json['id'], "endpoint": request.json['endpoint'], "chat_id": contact}
        response = r.post(f"{dataHandler_host}{api_route}", json=request_data, timeout=10.0)

    try:
        response.raise_for_status()
    except Exception:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when adding new endpoint'}), 500)

    # Successful response
    return make_response(jsonify({'status': 'success',}), 200)



@app.route('/contact/get/<string:account_id>', methods=['GET'])
def get_user_contacts(account_id):

    # Formulate request
    api_route = '/account/contact/get'
    request_data = {'account_id' : account_id}

    try:
        response = r.get(f"{dataHandler_host}{api_route}", json=request_data, timeout=10.0)
    except TimeoutError:
        print("Request to the backend API has timed out")
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when retrieving contacts'}), 500)

    try:
        response.raise_for_status()
    except Exception:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when retrieving contacts'}), 500)

    # Successful response
    return make_response(jsonify(response.json()), 200)



@app.route('/watchlist/remove', methods=['POST'])
def remove_account_watchlist():

    required_fields = ['id', 'endpoint']
    api_route = '/endpoint/remove'

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    request_data = {'account_id': request.json['id'], 'endpoint': request.json['endpoint']}

    try:
        response = r.delete(f"{dataHandler_host}{api_route}", json=request_data, timeout=10.0)
    except TimeoutError:
        print("Request to the backend API has timed out")
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when retrieving contacts'}), 500)

    try:
        response.raise_for_status()
    except Exception:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when retrieving contacts'}), 500)

    # Successful response
    return make_response(jsonify({'status': 'success',}), 200)



if __name__ == '__main__':
    print("Watchlist service is running...")
    app.run(host="esdwatchdog.com", port=5001, debug=True)