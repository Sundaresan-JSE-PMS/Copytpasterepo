from flask import Flask, json, jsonify, request, Response
import requests
from flask_cors import CORS
from flask_sock import Sock
from websocket import create_connection
import json

api = Flask(__name__)
sock = Sock(api)
CORS(api)

url2 = "https://neolife-sentinel.eu.auth0.com/oauth/token"
headers = {
        "content-type": "application/json",
        }
data = {
        "client_id": "vZBOUOa3otqtjiLhXg1huMDkGax4MPki",
        "client_secret": "MXRN4xv75__oEon2zRbCgncIVG0nTwQxCXD8L6cG0lCVRoPQgNApVgHlq52uvd2a"
,
        "audience": "https://neolife-sentinel.eu.auth0.com/api/v2/",
        "grant_type": "client_credentials",
        }
response = requests.post(url2, headers=headers, json=data)
access_token = response.json()["access_token"]


@api.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if 'username' in data and 'password' in data and 'role' in data and 'organization' in data:
            username = data['username']
            password = data['password']
            email = data['email']
            role = data['role']
            organization = data['organization']

            url = "https://neolife-sentinel.eu.auth0.com/api/v2/users"
            payload = json.dumps({
                "email": email,
                "email_verified": False,
                "app_metadata": {
                    "role": role,
                    "organization": organization
                },
                "name": username,
                "connection": "Username-Password-Authentication",
                "password": password,
                "verify_email": True  # Set to True to trigger email verification
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'authorization': 'Bearer ' + access_token
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 201:
                # After creating the user, trigger email verification
                user_id = response.json().get('user_id')
                verification_url = f"https://neolife-sentinel.eu.auth0.com/api/v2/users/{user_id}"
                verification_payload = {"email_verified": False}
                verification_response = requests.patch(verification_url, headers=headers, json=verification_payload)

                if verification_response.status_code == 200:
                    return jsonify({'message': f'User {username} created successfully. Email verification triggered'}), 201
                else:
                    return jsonify({'message': f'User {username} created, but email verification failed'}), 500

            else:
                return jsonify({'message': f'User with username: {username} create failed due to {response.reason}'}), response.status_code
        else:
            return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/list', methods=['POST'])
def list_users():
    try:
        data = request.get_json()
        if 'organization' in data:
            organization = data['organization']
            url = f'https://neolife-sentinel.eu.auth0.com/api/v2/users?q=app_metadata.organization={organization}'
           
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'authorization': 'Bearer ' + access_token
            }
            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify({'message': f'Error {response.reason}'}), response.status_code
        else:
            return jsonify({'error': 'Invalid request. Missing organizationId parameter.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a user
@app.route('/delete/<userID>', methods=['DELETE'])
def delete_user(userID):

    url = 'https://neolife-sentinel.eu.auth0.com/api/v2/users/'+userID
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Bearer '+access_token
    }
    payload={}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.status_code==204:
        return jsonify({'message': f'User with UserID: {userID} deleted successfully'}), 200
    else:
        return jsonify({'message': f'User with UserID: {userID} delete failed due to {response.reason}'}), response.status_code


# Rename a user 
@api.route('/rename/<userID>', methods=['PUT'])
def rename_user(userID):
    data = request.get_json()
    api.logger.info(f"Received request to update user with UserID: {userID}")
    if data:
        url = 'https://neolife-sentinel.eu.auth0.com/api/v2/users/'+userID
        
        # Remove the 'username' field and use 'name' instead
        data["name"] = data.pop("username", None)
        data["connection"] = "Username-Password-Authentication"
        payload = data

        print('Received PUT request with payload:', request.get_json())
        print('Final Payload:', payload)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'authorization': 'Bearer '+access_token
        }
        print('Request Headers:', headers)
        response = requests.patch(url, headers=headers, json=payload)
        print('Auth0 API Response:', response.text) 
        if response.status_code==200:
            return jsonify({'message': f'User with UserID: {userID} updated successfully'}), 200
        else:
            return jsonify({'message': f'User with UserID: {userID} update failed due to {response.reason}'}), response.status_code
    else:
        return jsonify({'error': f'User with UserID: {userID} not found'}), 404













@api.route('/', defaults={'path': ''})
@api.route('/<path:path>', methods=['GET','PUT','POST','DELETE'])
def getAnything(path):
    url = "http://pmsind.co.in:9444/fhir-server/api/v4"
    path = request.path
    params = request.query_string.decode('utf-8')
    fullurl = url+path+params
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authorization': 'Basic ZmhpcnVzZXI6Y2hhbmdlLXBhc3N3b3Jk'
    }
    if request.method == 'GET':
        initialResponse = requests.get(fullurl, headers=headers)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'con
nection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() 
if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "PUT":
        data = request.get_json()
        initialResponse = requests.put(fullurl, headers=headers, data=json.dumps(data))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'con
nection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() 
if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "POST":
        data = request.get_json()
        initialResponse = requests.post(fullurl, headers=headers, data=json.dumps(data))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'con
nection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() 
if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "DELETE":
        initialResponse = requests.delete(fullurl, headers=headers)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'con
nection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() 
if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response


@sock.route('/notification')
def echo(sock):
    ws = create_connection("ws://pmsind.co.in:9444/fhir-server/api/v4/notification")
    while True:
        result = ws.recv()
        sock.send(result)

if __name__ == '__main__':
    cert_file = 'cert.pem'
    key_file = 'privkey.pem'
    api.run(host='0.0.0.0',port=5000,ssl_context=(cert_file,key_file),debug=True)
