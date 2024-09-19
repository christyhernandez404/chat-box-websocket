from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO()

socketio.init_app(app, cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    print('Client Connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('message')
def handle_message(message_data):
    user_agent = request.headers.get('User-Agent','')
    print(f"User-Agent: {user_agent}") 

    if not user_agent:
        username = 'Postman User'
    else:
        username = 'Browser User'
    
    if isinstance(message_data, str):
        text = message_data
    else:
        text = message_data.get('text', '')
    
    socketio.emit("message",{'username': username, 'text': text})

@app.route("/")
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)