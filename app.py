from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# --- Game Data (Expanded List) ---
PROMPTS = [
    {"prompt": "Donald Duck's middle name.", "answer": "Fauntleroy"},
    {"prompt": "A study published in the journal Anthrozoo reported that cows produce 5% more milk when they are given _____.", "answer": "Names"},
    {"prompt": "In 2002, Bruce Willis sent 12,000 boxes of _____ to U.S. soldiers in Afghanistan.", "answer": "Girl Scout Cookies"},
    {"prompt": "The original name for the search engine Google was _____.", "answer": "Backrub"},
    {"prompt": "In the 19th century, it was fashionable for wealthy Europeans to have _____ as pets.", "answer": "Hermits"},
    {"prompt": "In Switzerland, it is illegal to own just one _____.", "answer": "Guinea pig"},
    {"prompt": "A group of flamingos is called a _____.", "answer": "Flamboyance"},
    {"prompt": "The tiny plastic or metal tube at the end of a shoelace is called an _____.", "answer": "Aglet"},
    {"prompt": "The Roman emperor Caligula once declared war on _____.", "answer": "The sea"},
    {"prompt": "Before the 17th century, carrots were _____.", "answer": "Purple"},
    {"prompt": "The dot over the letter 'i' and 'j' is called a _____.", "answer": "Tittle"},
    {"prompt": "The unicorn is the national animal of _____.", "answer": "Scotland"},
]

# --- Game State ---
game_state = {
    "prompt": "",
    "answer": "",
    "answers": [],
    "stage": "waiting"  # waiting -> answering -> voting
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@socketio.on('connect')
def handle_connect():
    # Send the current game state to a newly connected client
    emit('game_update', game_state)

@socketio.on('get_random_prompt')
def handle_get_random_prompt():
    selected = random.choice(PROMPTS)
    # Emit only to the admin who requested it
    emit('random_prompt_data', selected, room=request.sid)

@socketio.on('start_game')
def handle_start_game(data):
    game_state['prompt'] = data.get('prompt')
    game_state['answer'] = data.get('answer')
    game_state['stage'] = 'answering'
    game_state['answers'] = []
    socketio.emit('game_update', game_state)

@socketio.on('submit_answers')
def handle_submit_answers(data):
    player_answers = data.get('player_answers', [])
    
    # Add the real answer to the list of player answers
    all_answers = player_answers + [game_state['answer']]
    random.shuffle(all_answers)
    
    game_state['answers'] = all_answers
    game_state['stage'] = 'voting'
    socketio.emit('game_update', game_state)

@socketio.on('new_round')
def handle_new_round():
    game_state['stage'] = 'waiting'
    game_state['prompt'] = ''
    game_state['answer'] = ''
    game_state['answers'] = []
    socketio.emit('game_update', game_state)

if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible on your local network
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)