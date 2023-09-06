from flask import Flask, render_template, request
from flask_socketio import SocketIO
import openai
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

openai.api_key = os.getenv("OAIKEY")

# Global chat history
global_history = [{"role": "system", "content": "You are a patient undergoing psychoanalytic therapy."}]

@app.route('/')
def index():
    role = request.args.get('role', 'user')  # Defaults to 'user' if no 'role' parameter is present
    return render_template('index.html', role=role)

@socketio.on('new_message')
def handle_new_message(msg, methods=['GET', 'POST']):
    print('received message: ' + msg)

    global global_history

    global_history.append({"role": "user", "content": msg})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=global_history
    )

    reply = response["choices"][0]["message"]["content"]
    global_history.append({"role": "assistant", "content": reply})

    socketio.emit('new_message', reply)

if __name__ == '__main__':
    socketio.run(app, debug=True)
