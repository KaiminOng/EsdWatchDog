from flask import Flask, request, make_response, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/1129690128:AAFzGAL-Rur8QAZyjG2_62f5tvQvOKjv29w', methods=['GET', 'POST'])
def listener():

    # Check if incoming request is json
    if request.is_json:
    
        # Parse request data into json
        parsed_req = request.json
        update_type_index = {'left_chat_participant' : 'remove', 'new_chat_participant' : 'add'}

        # Define endpoints
        datahandler_host = os.environ.get('DH_URI')
        endpoint_index = {'add' : f'{datahandler_host}/account/contact/new', 'remove': f'{datahandler_host}/account/contact/remove'}

        # Get chat information
        chat_info = parsed_req['message']['chat']
        chat_id = chat_info['id']
        chat_type = chat_info['type']
        chat_title = chat_info.get('title', 'private')

        # Get sender information
        user_id = parsed_req['message']['from']['id']

        # Get update type; Check if /start command initiated by user
        update_type = 'add' if 'text' in parsed_req['message'] and parsed_req['message']['text'] == '/watchdog' else False

        # Get update type and respective endpoint 
        for key, value in update_type_index.items():
            if key in parsed_req['message']:
                update_type = value
                break
        
        # Send add contact request
        if update_type == 'add':
            request_data = {'account_id' : user_id, 'chat_id' : chat_id, 'chat_title' : chat_title, 'chat_type' : chat_type}
            response = requests.post(endpoint_index[update_type], json=request_data)

        elif update_type == 'remove':
            request_data = {'account_id' : user_id, 'chat_id' : chat_id}
            response = requests.delete(endpoint_index[update_type], json=request_data)


        if update_type:
            try:
                print(f"Received at incoming {update_type} request!")
                response.raise_for_status()
            except Exception:
                print(f"Status code: {response.status_code}")
        
        print("Update operation successful!")

    # Incoming request is not JSON
    else:
        return make_response(jsonify({'invalid data format'}), 400)
    
    return make_response("Update received!", 200)

if __name__ == '__main__':
    print("Bot-tracker is running...")
    app.run(ssl_context=('PUBLIC.pem', 'PRIVATE.key'), host='0.0.0.0', port='8443')