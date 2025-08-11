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
    {"prompt": "The _____ is the national animal of Scotland.", "answer": "Unicorn"},
    {"prompt": "On November 12, 1970, George Thornton, a highwat engineer in Oregon, had the unusual job of blowing up a _____.", "answer": "Dead Whale"},
    {"prompt": "People in Damariscotta, Maine hold an annual race where they use _____ as boats.", "answer": "Pumpkins"},
    {"prompt": "As a young student in Buenos Aires, Pope Francis worked as a _____.", "answer": "Bouncer"},
    {"prompt": "A woman in Muncie, Indiana was hospitalized after trying to remove a callus on her foot with a _____.", "answer": "Shotgun"},
    {"prompt": "Jacobite Cruises purchased unusual insurance to protect it from damage caused by _____.", "answer": "The Loch Ness Monster"},
    {"prompt": "El Colacho is a Spanish festival where people dress up like the devil and jump over _____.", "answer": "Babies"},
    {"prompt": "Cheap Chic Weddings is an annual contest in which participants make wedding dresses out of _____.", "answer": "Toilet Paper"},
    {"prompt": "Marcella Hazan is the culinary guru who pioneered the unusual technique of cooking duck with a _____.", "answer": "Hair Dryer"},
    {"prompt": "The sound of E.T. walking was made by someone squishing _____.", "answer": "Jell-O"},
    {"prompt": "The first item listed on eBay was a broken _____.", "answer": "Laser Pointer"},
    {"prompt": "Oddly enough, Albert Einstein's eyeballs can be found in a _____ in New York City.", "answer": "Safe Deposit Box"},
    {"prompt": "In 2013, a wealthy Michagan man bought the house next to his ex -wife and erected a giant bronze statue of a _____.", "answer": "Middle Finger"},
    {"prompt": "The name of the first chimp sent into space.", "answer": "Ham"},
    {"prompt": "The name for a group of porcupines", "answer": "Prickle"},
    {"prompt": "The name of the dog that won the 2012 World's Ugliest Dog Competition.", "answer": "Mugly"},
    {"prompt": "Dr. Seuss is credit with coining this common derogatory term in his 1950 book If I Ran the Zoo.", "answer": "Nerd"},
    {"prompt": "The name of the man on the Quaker Oats label.", "answer": "Larry"},
    {"prompt": "During a famous fire in 1567, a Norwegian man named Hans Steininger died after tripping over a _____.", "answer": "Beard"},
    {"prompt": "The fishing company E21 makes a very peculiar fishing rod that is composed of 70% _____.", "answer": "Carrots"},
    {"prompt": "On January 13, 2014, U.S. Secretary of State John Kerry presented to Russian Foreign Minister Sergei Lavrow the odd gift of two very large _____.", "answer": "Potatoes"},
    {"prompt": "During the mid to late-nineties, the English town of Glastonbury was on a manhunt for the old house intruder known as 'The _____.'", "answer": "Tickler"},
    {"prompt": "Suffering from an extremely rare side effect after getting hip surgery in 2010, a Dutch man has alienated his family because he cannot stop _____.", "answer": "Laughing"},
    {"prompt": "It's weird work but Jackie Samuel charges $60 an hour to _____.", "answer": "Snuggle"},
    {"prompt": "Huggies Brazil developed a phone app that tells you when a baby's diaper is wet. It's called _____.", "answer": "Tweetpee"},
    {"prompt": "Ben and Jerry only started making ice cream because it was too expensive to make _____.", "answer": "Bagels"},
    {"prompt": "Tashirojima is an island off of Japan that is complete overrun by _____.", "answer": "Cats"},
    {"prompt": "While president of the United States, John Adams had a dog named Juno and a dog named _____.", "answer": "Satan"},
    {"prompt": "In 2012, a 26-year-old man from London went on a mission to lick every _____ in the United Kingdom.", "answer": "Cathedral"},
    {"prompt": "In 2003, Morocco made the highly unusual offer to send 2,000 _____ to assist the United States' war efforts in Iraq.", "answer": "Monkeys"},
    {"prompt": "Romano Mussolini, son of the fascist dictator Benito Mussolini, did not follow in his father's footsteps. Instead, he made his living as a _____.", "answer": "Jazz Musician"},
    {"prompt": "ROAD TRIP! When in Nepal, visit the village of Parsawa and Laxmipur, where you can enjoy the slightly off-putting 10 day _____ Festival.", "answer": "Cursing"},
    {"prompt": "A group known as the 'Robin Hooders' in Keene, New Hampshire pay for other people's _____.", "answer": "Parking Meters"},
    {"prompt": "In an effort to push 'slow TV,' Norway had a 12-hour block of programming in 2013 dedicated to _____.", "answer": "Knitting"},
    {"prompt": "Belmont University in Nashville has offered a class called 'Oh, Look, a _____.'", "answer": "Chicken"},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
    {"prompt": "", "answer": ""},
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