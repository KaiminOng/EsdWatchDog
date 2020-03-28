from flask import make_response, jsonify, request


def validate_request(request, required_fields : list):
    # Check if request is of MIME type JSON

    try:
        data = request.get_json()
    except Exception:
        print("Received request is not JSON")
        raise ValidationError('error', 'Received request is not JSON', 401)

    # Check if request contains the required headers
    for field_name in required_fields:
        if field_name not in data.keys():
            print(f"{field_name} field is missing in request")
            raise ValidationError('error', f"{field_name} field is missing in request", 401)


class ValidationError(Exception):
    """Raised when incoming request fails basic validation"""
    def __init__(self, status, message, http_status_code):
        self.status = status
        self.message = message
        self.http_status_code = http_status_code 