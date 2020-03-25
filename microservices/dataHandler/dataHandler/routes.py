from flask import request, make_response, jsonify
from flask import current_app as app
from .models import Account, Endpoint, Contact, db
from .validator import validate_request

# Create a new account
@app.route('/account/new', methods=['POST'])
def register_account():

    # Specify the required fields to be present in the request
    required_fields = ['id', 'username']
    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        print(e.message)
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)

    new_user = Account(request.json['id'], request.json['username'])
    db.session.add(new_user)

    # Commit changes to database
    try:
        db.session.commit()
    # Error during commit
    except Exception as e:
        print('Error when adding new user to database')
        return make_response(jsonify({'status' : 'error', 'message' : 'Error when creating account'}), 500)

    # Account creation successful    
    return make_response(jsonify({'status' : 'success'}), 200)


# Get account endpoints
# @app.route('/endpoint/<:id>', methods=['GET'])






