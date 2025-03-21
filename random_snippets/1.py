from flask import Flask, request, jsonify
from urllib3.exceptions import InsecureRequestWarning
import requests
import json


app = Flask(__name__)

@app.route('/DiaManT/api/internal/dialogs', methods=['POST'])
def handle_dialog_request():
    data = request.get_json()
    target_api_url = 'https://0.0.0.0:8443/DiaManT/api/internal/dialogs?compact=True'
    headers = request.headers
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(target_api_url, json=data, headers=headers, verify=False)
    return json.dumps(response.json(), ensure_ascii=False), response.status_code
 
@app.route('/DiaManT/api/internal/dialogs/<dialog_id>', methods=['POST'])
def handle_specific_dialog_request(dialog_id):
    application_id = request.json.get('application_id', 'default_application_id')
    utterance = request.json.get('utterance', 'default_utterance')      
    print("prishlo : " + utterance)
    data = {
        'application_id': application_id,
        'utterance': utterance
    }
    print(data)
    target_api_url = f'https://0.0.0.0:8443/DiaManT/api/internal/dialogs/{dialog_id}?compact=True'
    headers = request.headers
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(target_api_url, json=data, headers=headers, verify=False)
    try:
        print(response.json().get('prompt'))
    except Exception:
        print('диалог скорее всего завершился')
    return json.dumps(response.json(), ensure_ascii=False), response.status_code
    
@app.route('/DiaManT/api/internal/dialogs/', methods=['POST'])
def handle_dialog_request2():
    data = request.get_json()
    target_api_url = 'https://0.0.0.0:8443/DiaManT/api/internal/dialogs?compact=True'
    headers = request.headers
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(target_api_url, json=data, headers=headers, verify=False)
    return json.dumps(response.json(), ensure_ascii=False), response.status_code
 
@app.route('/DiaManT/api/internal/dialogs/<dialog_id>/', methods=['POST'])
def handle_specific_dialog_request2(dialog_id):
    application_id = request.json.get('application_id', 'default_application_id')
    utterance = request.json.get('utterance', 'default_utterance')    
    print("prishlo : " + utterance)
    data = {
        'application_id': application_id,
        'utterance': utterance
    }
    print(data)
    target_api_url = f'https://0.0.0.0:8443/DiaManT/api/internal/dialogs/{dialog_id}?compact=True'
    headers = request.headers
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(target_api_url, json=data, headers=headers, verify=False)
    try:
        print(response.json().get('prompt'))
    except Exception:
        print('диалог скорее всего завершился')
    return json.dumps(response.json(), ensure_ascii=False), response.status_code

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8453, debug=False) 
