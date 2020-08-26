from flask import Flask, render_template, request, redirect, url_for, make_response
from urllib.parse import quote
import time
import socket
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import AssistantV2
import json

# import motors
# import sensor
# import arm
# import AI
# motors.stop()
# Get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()
import yaml

with open('apikey.yml') as f:
    data_of_yml = yaml.load(f, Loader=yaml.FullLoader)
    assistant_api_key = data_of_yml.get('assisstant').get('apikey')
    assistant_url = data_of_yml.get('assisstant').get('url')
    assisstant_id = data_of_yml.get('assisstant').get('assisstant_id')

app = Flask(__name__)
def assistant(question):
    authenticator = IAMAuthenticator(assistant_api_key)
    assistant = AssistantV2(
        version='2020-04-01',
        authenticator=authenticator
    )
    message_input = question
    message_input.encode('utf-8')
    assistant.set_service_url(assistant_url)
    session_id = assistant.create_session(
        assistant_id=assisstant_id
    ).get_result()
    session_idj = json.dumps(session_id['session_id'])[1: -1]
    response = assistant.message(
        assistant_id=assisstant_id,
        session_id=session_idj,
        input={
            'message_type': 'text',
            'text': message_input
        }
    ).get_result()
    response_of_assistant = json.loads(json.dumps(response['output']['generic'][0]['text']))
    print(response_of_assistant)
    return response_of_assistant


@app.route('/')
def my_form():
    templateData = {
        'Response': "waiting",
    }
    return render_template('index.html', **templateData ,server_ip=server_ip)


@app.route('/', methods=["GET", "POST"])
def my_form_post():
    Response = ""
    text = request.form['text']
    processed_text = text.upper()
    processed_textx =assistant(processed_text)
    templateData = {
        'Response': processed_textx
    }


    return render_template('index.html', **templateData)


app.run(debug=True, host='0.0.0.0', port=8000)
