from flask import request, make_response, jsonify
from flask import current_app as app
from .models import Account, Endpoint, Contact, db, Monitoring, accountEndpoint
from .helper import get_or_create
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

    new_user = Account(id=request.json['id'], username=request.json['username'])
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
@app.route('/endpoint/get/<string:account_id>', methods=['GET'])
def get_endpoints(account_id):

    # Get user object
    account = Account.query.filter_by(id=account_id).first_or_404(description=f'Specified user id was not found: {account_id}')
    endpoints = [x.endpoint_url for x in account.watchlist]

    return make_response(jsonify({
        'status' : 'success',
        'result' : endpoints
    }), 200)


# Add new endpoint for user
@app.route('/endpoint/new', methods=['POST'])
def register_endpoint():

    # Specify the required fields to be present in the request
    required_fields = ['id', 'endpoint', 'chat_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)


    # Add prerequisite entries to account, endpoint and contact tables
    account = get_or_create(db.session, Account, id=request.json['id'])
    endpoint = get_or_create(db.session, Endpoint, endpoint_url=request.json['endpoint'])

    # Create a new entry in the associative table
    new_accountEndpoint = accountEndpoint(account_id=request.json['id'], endpoint_url=request.json['endpoint'], chat_id=request.json['chat_id'])

    try:
        # Add and commit the changes
        db.session.add(new_accountEndpoint)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status' : 'error', 'message' : 'Error occured when registering an endpoint'}), 500)

    return make_response(jsonify({'status' : 'success'}), 200)


# Register new event 
@app.route('/endpoint/event/new', methods=['POST'])
def register_event():

    required_fields = ['events']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)

    # loop through array
    for event in request.json['events']:
        new_event = Monitoring(endpoint_url=event['endpoint'], timestamp=event['timestamp'], status=event['status'])
        db.session.add(new_event)

    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status' : 'error', 'message' : 'Error occured when registering endpoint'}), 500)

    return make_response(jsonify({'status' : 'success'}), 200)


# Get events for endpoint
@app.route('/endpoint/event', methods=['GET'])
def get_events():

    result = dict()

    # Specify the required fields to be present in the request
    required_fields = ['endpoint']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)
    
    endpoint_array = [request.json['endpoint']] if not isinstance(request.json['endpoint'], list) else request.json['endpoint']

    # Get endpoint object ; throws error 404 if endpoint not found
    for endpoint in endpoint_array:
        get_endpoint = Endpoint.query.filter_by(endpoint_url=endpoint).first_or_404(description=f'Specified endpoint was not found: {endpoint}')
        result[endpoint] = [{"status": x.status, "timestamp": x.timestamp} for x in get_endpoint.events]

    # Return success response
    return make_response(jsonify({
        'status' : 'success',
        'result' : result
    }), 200)


# Update status of endpoints
@app.route('/endpoint/status', methods=['PATCH'])
def update_endpoint_status():

    # Specify the required fields to be present in the request
    required_fields = ['report']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)

    for record in request.json['report']:
        try:
            endpoint_row = Endpoint.query.filter_by(endpoint_url=record["endpoint"]).first_or_404()
        except Exception:
            # Go to next record in report if endpoint does not exist
            continue
        endpoint_row.update_status(record['status'], record['timestamp'])

    # Update rows in endpoint table
    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status' : 'error', 'message' : 'Error occured when updating endpoint status'}), 500)

    # Return success response
    return make_response(jsonify({'status' : 'success'}), 200)


# Get all endpoints for healthcheck
@app.route('/endpoint/dump', methods=['GET'])
def dump_endpoints():

    result = dict()

    for endpoint in Endpoint.query.all():
        result[endpoint.endpoint_url] = endpoint.status

    return make_response(jsonify({
        'status' : 'success',
        'result' : result
    }), 200)
    

# Register new chat 
@app.route('/contact/new', methods=['POST'])
def register_contact():

    required_fields = ['chat_id', 'chat_title', 'chat_type', 'account_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)

    # Create new Contact object
    new_contact = Contact(chat_id=request.json['chat_id'], chat_title=request.json['chat_title'], chat_type=request.json['chat_type'], chat_owner_id=request.json['account_id'])
    db.session.add(new_contact)

    # Update rows in contact table
    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status' : 'error', 'message' : 'Error occured when adding new contact'}), 500)

    # Return success response
    return make_response(jsonify({'status' : 'success'}), 200)


# Delete chat 
@app.route('/contact/remove', methods=['DELETE'])
def remove_contact():

    required_fields = ['chat_id', 'account_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status' : e.status, 'message' :e.message}), e.http_status_code)

    # Get chat_id to delete 
    contact = Contact.query.filter_by(chat_id=request.json['chat_id'], chat_owner_id=request.json['account_id']).first_or_404(description='Specified contact was not found!')

    # Commit changes
    try:
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status' : 'error', 'message' : 'Error occured when removing contact'}), 500)

    # Return success response
    return make_response(jsonify({'status' : 'success'}), 200)

# Edit endpoint 

# Delete endpoint

# Get user available chat groups




