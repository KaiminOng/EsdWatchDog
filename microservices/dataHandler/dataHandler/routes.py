from flask import request, make_response, jsonify
from flask import current_app as app
from .models import Account, Endpoint, Contact, db, Monitoring, accountEndpoint
from .helper import get_or_create
from .validator import validate_request


# Create a new account
@app.route('/account/new', methods=['POST'])
def register_account():

    # Specify the required fields to be present in the request
    required_fields = ['account_id', 'username']
    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        print(e.message)
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    new_user = Account(id=request.json['account_id'],
                       username=request.json['username'])
    db.session.add(new_user)

    # Commit changes to database
    try:
        db.session.commit()
    # Error during commit
    except Exception as e:
        print('Error when adding new user to database')
        return make_response(jsonify({'status': 'error', 'message': 'Error when creating account'}), 500)

    # Account creation successful
    return make_response(jsonify({'status': 'success'}), 200)


# Get account endpoints for watchlist
@app.route('/endpoint/get', methods=['GET'])
def get_endpoints():

    required_fields = ['account_id']

    inserted_endpoints = []

    result = []

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    account_id = request.json['account_id']

    # Get user object
    account = Account.query.filter_by(id=account_id).first_or_404(
        description=f'Specified user id was not found: {account_id}')

    for accountEndpoint in account.watchlist:
        endpoint_object = accountEndpoint.endpoint
        if endpoint_object.endpoint_url not in inserted_endpoints:

            # Get contacts for the endpoint
            contacts = accountEndpoint.query.filter_by(account_id=account_id, endpoint_url=endpoint_object.endpoint_url).all()
            
            result.append({"endpoint": endpoint_object.endpoint_url, "status": endpoint_object.status, "last_checked": endpoint_object.last_checked, "events": [
                          {"status": x.status, "timestamp": x.timestamp} for x in endpoint_object.events], "contacts": [{'chat_id': c.contact.chat_id, 'chat_title': c.contact.chat_title} for c in contacts]})

            inserted_endpoints.append(endpoint_object.endpoint_url)

    return make_response(jsonify({
        'status': 'success',
        'result': result
    }), 200)


# Add new endpoint for user
@app.route('/endpoint/new', methods=['POST'])
def register_endpoint():

    # Specify the required fields to be present in the request
    required_fields = ['account_id', 'endpoint', 'chat_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Add prerequisite entries to account, endpoint and contact tables
    account = get_or_create(db.session, Account, id=request.json['account_id'])
    endpoint = get_or_create(db.session, Endpoint,
                             endpoint_url=request.json['endpoint'])

    for contact in request.json['chat_id']:
        # Create a new entry in the associative table
        new_accountEndpoint = accountEndpoint(account_id=request.json['account_id'], endpoint_url=request.json['endpoint'], chat_id=contact)
        db.session.add(new_accountEndpoint)

    try:
        # Add and commit the changes
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when registering an endpoint'}), 500)

    return make_response(jsonify({'status': 'success'}), 200)


# Register new event
@app.route('/endpoint/event/new', methods=['POST'])
def register_event():

    required_fields = ['events']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # loop through array
    for event in request.json['events']:
        new_event = Monitoring(
            endpoint_url=event['endpoint'], timestamp=event['timestamp'], status=event['status'])
        db.session.add(new_event)

    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when registering endpoint'}), 500)

    return make_response(jsonify({'status': 'success'}), 200)


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
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    endpoint_array = [request.json['endpoint']] if not isinstance(
        request.json['endpoint'], list) else request.json['endpoint']

    # Get endpoint object ; throws error 404 if endpoint not found
    for endpoint in endpoint_array:
        get_endpoint = Endpoint.query.filter_by(endpoint_url=endpoint).first_or_404(
            description=f'Specified endpoint was not found: {endpoint}')
        result[endpoint] = [
            {"status": x.status, "timestamp": x.timestamp} for x in get_endpoint.events]

    # Return success response
    return make_response(jsonify({
        'status': 'success',
        'result': result
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
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    for record in request.json['report']:
        try:
            endpoint_row = Endpoint.query.filter_by(
                endpoint_url=record["endpoint"]).first_or_404()
        except Exception:
            # Go to next record in report if endpoint does not exist
            continue
        endpoint_row.update_status(record['status'], record['timestamp'])

    # Update rows in endpoint table
    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when updating endpoint status'}), 500)

    # Return success response
    return make_response(jsonify({'status': 'success'}), 200)


# Get all endpoints for healthcheck
@app.route('/endpoint/dump', methods=['GET'])
def dump_endpoints():

    result = dict()

    for endpoint in Endpoint.query.all():
        result[endpoint.endpoint_url] = endpoint.status

    return make_response(jsonify({
        'status': 'success',
        'result': result
    }), 200)


# Register new chat
@app.route('/account/contact/new', methods=['POST'])
def register_account_contact():

    required_fields = ['chat_id', 'chat_title', 'chat_type', 'account_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Create new Contact object
    new_contact = Contact(chat_id=request.json['chat_id'], chat_title=request.json['chat_title'],
                          chat_type=request.json['chat_type'], chat_owner_id=request.json['account_id'])
    db.session.add(new_contact)

    # Update rows in contact table
    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when adding new contact'}), 500)

    # Return success response
    return make_response(jsonify({'status': 'success'}), 200)


# Delete chat; Used when bot is removed from chat
@app.route('/account/contact/remove', methods=['DELETE'])
def remove_account_contact():

    required_fields = ['chat_id', 'account_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Get all child rows
    child_rows = accountEndpoint.query.filter_by(account_id=request.json['account_id'], chat_id=request.json['chat_id']).delete()

    # Get chat_id to delete
    contact = Contact.query.filter_by(chat_id=request.json['chat_id'], chat_owner_id=request.json['account_id']).first_or_404(
        description='Specified contact was not found!')

    # Commit changes
    try:
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        # raise e
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when removing contact'}), 500)

    # Return success response
    return make_response(jsonify({'status': 'success'}), 200)


# Delete contact for specific endpoint
@app.route('/endpoint/contact/remove', methods=['DELETE'])
def remove_endpoint_contact():

    required_fields = ['chat_id', 'account_id', 'endpoint']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Get chat_id to delete
    row = accountEndpoint.query.filter_by(endpoint_url=request.json['endpoint'], account_id=request.json['account_id'], chat_id=request.json['chat_id']).first_or_404(
        description='Specified record was not found!')

    # Commit changes
    try:
        db.session.delete(row)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when removing contact'}), 500)

    # Return success response
    return make_response(jsonify({'status': 'success'}), 200)


# Edit endpoint; Only allow user to edit chat_id

# Delete endpoint
@app.route('/endpoint/remove', methods=['DELETE'])
def remove_account_endpoint():

    required_fields = ['account_id', 'endpoint']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    # Get rows to delete
    accountEndpoint.query.filter_by(account_id=request.json['account_id'], endpoint_url=request.json['endpoint']).delete()

    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when removing contact'}), 500)

    # Remove parent if no more references
    try:
        # If no more users tracking the endpoint
        accountEndpoint.query.filter_by(endpoint_url=request.json['endpoint']).first_or_404()
    except Exception:
        # Delete monitoring records
        Monitoring.query.filter_by(endpoint_url=request.json['endpoint']).delete()
        # Delete from endpoint table
        Endpoint.query.filter_by(endpoint_url=request.json['endpoint']).delete()

    try:
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': 'Error occured when removing endpoint record'}), 500)

    # Return success response
    return make_response(jsonify({'status': 'success'}), 200)


# Get user available chat groups
@app.route('/account/contact/get', methods=['GET'])
def get_account_contacts():

    required_fields = ['account_id']

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    contacts = Contact.query.filter_by(chat_owner_id=request.json['account_id']).all()
    results = [{'chat_id': x.chat_id, 'chat_title': x.chat_title, 'chat_type': x.chat_type} for x in contacts]

    return make_response(jsonify({
        'status': 'success',
        'result': results
    }), 200)


# Get all contacts for each endpoint
@app.route('/endpoint/contact/get', methods=['GET'])
def get_endpoint_contacts():

    required_fields = ['endpoint']

    results = []

    try:
        # Performs basic validation on request
        validate_request(request, required_fields)
    except Exception as e:
        return make_response(jsonify({'status': e.status, 'message': e.message}), e.http_status_code)

    for endpoint in request.json['endpoint']:
        target_chat = []
        associated = accountEndpoint.query.filter_by(endpoint_url=endpoint).all()
        for row in associated:
            if row.chat_id not in target_chat:
                target_chat.append(row.chat_id)
        results.append({'endpoint': endpoint, 'chat_id': target_chat})
        

    return make_response(jsonify({
        'status': 'success',
        'result': results
    }), 200)
