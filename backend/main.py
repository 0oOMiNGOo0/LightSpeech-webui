import os
import asyncio
import eventlet
import subprocess
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

@app.route('/uploaded', methods=['POST'])
def GETC():
    content = request.files['uploadFile']
    content.save('inference_text.txt')
    return jsonify({'test': 'ok'})

@app.route('/remove', methods=['POST'])
def AS():
    os.remove('inference_text.txt')
    return jsonify({'test': 'ok'})

@sio.on('uploaded')
def handle_message():
    command = "python lightspeech_inference.py --config configs/tts/lj/lightspeech.yaml --exp_name lightspeech --reset --inference_text inference_text.txt"
    subprocess.run(command, shell=True)

    path = os.path.expanduser("~")
    sio.send({'current':100, 'total': 100})
    if not os.path.exists(path + '/LightSpeech/output'):
        os.makedirs(path + '/LightSpeech/output')
    for i in os.listdir('output/wavs'):
        if os.path.exists(path + f'/LightSpeech/output/{i}'):
            os.replace(f'output/wavs/{i}', path + f'/LightSpeech/output/{i}')
        else:
            os.rename(f'output/wavs/{i}', path + f'/LightSpeech/output/{i}')
    output_paths = os.listdir(path + '/LightSpeech/output')
    print(output_paths)
    sio.emit('downloads', output_paths)
    os.remove('inference_text.txt')
    return

sio.run(app, host='0.0.0.0', port=5050, debug=True)