from flask import Flask, json, jsonify, request, Response
import requests
from flask_socketio import SocketIO, emit
from flask_sock import Sock
api = Flask(__name__)
sock = Sock(api)
url = "http://13.126.5.10:9444/fhir-server/api/v4"
@api.route('/<path:path>', methods=['GET'], defaults={'path': ''})
def getAnything(path):
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
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "PUT":
        data = request.get_json()
        initialResponse = requests.put(fullurl, headers=headers, data=json.dumps(data))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "POST":
        data = request.get_json()
        initialResponse = requests.put(fullurl, headers=headers, data=json.dumps(data))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response
    elif request.method == "DELETE":
        initialResponse = requests.delete(fullurl, headers=headers)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  initialResponse.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(initialResponse.content, initialResponse.status_code, headers)
        return response


if __name__ == '__main__':
    cert_file = './cert.pem'
    key_file = './privkey.pem'
    api.run(ssl_context=(cert_file,key_file),debug=True)
