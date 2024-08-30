import sys
import os
import json
import threading
import asyncio
import base64
from time import sleep
from random import choice
from flask import Flask, request, jsonify, send_file
import pyautogui
import mtranslate as mt
from dotenv import load_dotenv, set_key
from threading import Lock
from playsound import playsound
from Backend.Extra import AnswerModifier, QueryModifier, LoadMessages, GuiMessagesConverter
from Backend.Automation import Automation, professional_responses
from Backend.RSE_R import RealTimeChatBotAI
from Backend.Chatbot import ChatBotAI
from Backend.AutoModel import Model
from Backend.ChatGpt import ChatGptAI as ChatGptAI
from Backend.TTS2 import TTS
from Backend.RSE import Alert

Alert("JARVIS IS ONLINE NOW")

# Load environment variables
load_dotenv()
state = 'Available...'
messages = LoadMessages()
WEBCAM = False
js_messageslist = []
working: list[threading.Thread] = []
InputLanguage = os.environ['InputLanguage']
Assistantname = os.environ['AssistantName']
Username = os.environ['NickName']
lock = Lock()

app = Flask(__name__)

def UniversalTranslator(Text: str) -> str:
    """Translates text to English."""
    english_translation = mt.translate(Text, 'en', 'auto')
    return english_translation.capitalize()

def MainExecution(Query: str):
    """Main execution function for handling user queries."""
    global WEBCAM, state
    Query = UniversalTranslator(Query) if 'en' not in InputLanguage.lower() else Query.capitalize()
    Query = QueryModifier(Query)

    if state != 'Available...':
        return
    state = 'Thinking...'
    Decision = Model(Query)

    if 'general' in Decision or 'realtime' in Decision:
        if Decision[0] == 'general':
            if WEBCAM:
                # Placeholder for video capture function
                capture_image()
                sleep(0.5)
                Answer = AnswerModifier(ChatGptAI(Query))
            else:
                Answer = AnswerModifier(ChatBotAI(Query))
            state = 'Answering...'
            TTS(Answer)
        else:
            state = 'Searching...'
            Answer = AnswerModifier(RealTimeChatBotAI(Query))
            response = Answer
            state = 'Answering...'
            TTS(response)
    elif 'open webcam' in Decision:
        # Placeholder for starting video function
        start_video()
        playsound(r'Start.mp3')
        print('Video Started')
        WEBCAM = True
    elif 'close webcam' in Decision:
        # Placeholder for stopping video function
        stop_video()
        playsound(r'Stop.mp3')
        WEBCAM = False
    else:
        state = 'Automation...'
        asyncio.run(Automation(Decision, print))
        response = choice(professional_responses)
        state = 'Answering...'
        with open('ChatLog.json', 'w') as f:
            json.dump(messages + [{'role': 'assistant', 'content': response}], f, indent=4)
        TTS(response)
    state = 'Listening...'

@app.route('/messages', methods=['GET'])
def get_messages():
    """Fetches new messages to update the GUI."""
    global messages, js_messageslist
    with lock:
        messages = LoadMessages()
    if js_messageslist != messages:
        new_messages = GuiMessagesConverter(messages[len(js_messageslist):])
        js_messageslist = messages
        return jsonify(new_messages)
    return jsonify([])

@app.route('/state', methods=['GET', 'POST'])
def update_state():
    """Updates or retrieves the current state."""
    global state
    if request.method == 'POST':
        state = request.json.get('state')
    return jsonify({'state': state})

@app.route('/mic', methods=['POST'])
def handle_mic():
    """Handles microphone input."""
    transcription = request.json.get('transcription')
    print(transcription)
    if not working:
        work = threading.Thread(target=MainExecution, args=(transcription,), daemon=True)
        work.start()
        working.append(work)
    else:
        if working[0].is_alive():
            return jsonify({'status': 'working'})
        working.pop()
        work = threading.Thread(target=MainExecution, args=(transcription,), daemon=True)
        work.start()
        working.append(work)
    return jsonify({'status': 'started'})

@app.route('/start_video', methods=['POST'])
def start_video():
    """Starts the video capture."""
    # Replace this with actual video start logic
    # Example: start video capture using an external service or library
    print('Starting video capture...')
    return jsonify({'status': 'Video Started'})

@app.route('/stop_video', methods=['POST'])
def stop_video():
    """Stops the video capture."""
    # Replace this with actual video stop logic
    # Example: stop video capture using an external service or library
    print('Stopping video capture...')
    return jsonify({'status': 'Video Stopped'})

@app.route('/capture', methods=['POST'])
def capture_image():
    """Captures an image from the video."""
    # Replace this with actual image capture logic
    # Example: capture image from the video stream and save it
    print('Capturing image...')
    return jsonify({'status': 'Image Captured'})

@app.route('/page/<cpage>', methods=['GET'])
def navigate_page(cpage):
    """Navigates to the specified page."""
    if cpage == 'home':
        # Replace with actual home page logic
        print('Navigating to home page...')
    elif cpage == 'settings':
        # Replace with actual settings page logic
        print('Navigating to settings page...')
    return jsonify({'status': f'Navigated to {cpage}'})

@app.route('/setvalues', methods=['POST'])
def set_values():
    """Sets API keys and user preferences."""
    GeminiApi = request.json.get('GeminiApi')
    HuggingFaceApi = request.json.get('HuggingFaceApi')
    GroqApi = request.json.get('GroqApi')
    AssistantName = request.json.get('AssistantName')
    Username = request.json.get('Username')
    print(f'GeminiApi = {GeminiApi!r} HuggingFaceApi = {HuggingFaceApi!r} GroqApi = {GroqApi!r} AssistantName = {AssistantName!r} Username = {Username!r}')
    if GeminiApi:
        set_key('.env', 'CohereAPI', GeminiApi)
    if HuggingFaceApi:
        set_key('.env', 'HuggingFaceAPI', HuggingFaceApi)
    if GroqApi:
        set_key('.env', 'GroqAPI', GroqApi)
    if AssistantName:
        set_key('.env', 'AssistantName', AssistantName)
    if Username:
        set_key('.env', 'NickName', Username)
    return jsonify({'status': 'Values Set'})

@app.route('/setup', methods=['POST'])
def setup():
    """Sets up the GUI window."""
    pyautogui.hotkey('win', 'up')
    return jsonify({'status': 'Setup Complete'})

@app.route('/language', methods=['GET'])
def get_language():
    """Returns the input language."""
    return jsonify({'language': InputLanguage})

@app.route('/assistantname', methods=['GET'])
def get_assistant_name():
    """Returns the assistant's name."""
    return jsonify({'assistant_name': Assistantname})

@app.route('/capture_image', methods=['POST'])
def capture_image_route():
    """Saves the captured image."""
    image_data = request.json.get('image_data')
    image_bytes = base64.b64decode(image_data.split(',')[1])
    with open('capture.png', 'wb') as f:
        f.write(image_bytes)
    return jsonify({'status': 'Image Saved'})

if __name__ == '__main__':
    app.run(port=44444)
