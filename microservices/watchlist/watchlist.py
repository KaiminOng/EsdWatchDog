from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from validator import validate_request
import requests as r

# Start flask app
app = Flask(__name__)

dataHandler_host = 'http://localhost:5000'

@app.route('/watchlist/get', methods=['GET'])
def get_account_watchlist():

     # Specify the required fields to be present in the request
    required_fields = ['id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Formulate request
    api_route = '/endpoint/get'

    request_data = {'account_id' : request.json['id']}
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

    request_data = {'account_id' : request.json['id'], "endpoint": request.json['endpoint'], "chat_id": request.json['chat_id']}
    response = r.post(f"{dataHandler_host}{api_route}", json=request_data, timeout=10.0)

    try:
        response.raise_for_status()
    except Exception:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when adding new endpoint'}), 500)

    # Successful response
    return make_response(jsonify({'status': 'success',}), 200)



@app.route('/contact/get', methods=['GET'])
def get_user_contacts():

    # Specify the required fields to be present in the request
    required_fields = ['id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Formulate request
    api_route = '/account/contact/get'

    request_data = {'account_id' : request.json['id']}
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)