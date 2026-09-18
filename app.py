from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import threading
import time
import os

from core.network import get_local_ips
from core.game_manager import GameManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'partygamessecret!2026'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Single main room instance
game_mgr = GameManager(room_code="GAME")

# Background timer thread to keep timers synced across all screens
timer_running = True

def timer_loop():
    while timer_running:
        time.sleep(1.0)
        if game_mgr.state == "in_game":
            advanced = game_mgr.tick_timer()
            if advanced:
                broadcast_game_update()
            else:
                host_state = game_mgr.get_host_state()
                socketio.emit('host_update', host_state, room='host_room')

timer_thread = threading.Thread(target=timer_loop, daemon=True)
timer_thread.start()

def broadcast_game_update():
    """Broadcasts host state to host room and tailored state to players."""
    host_state = game_mgr.get_host_state()
    socketio.emit('host_update', host_state, room='host_room')
    
    # Broadcast to all player controllers
    socketio.emit('sync_request', room='players_room')

# --- HTTP Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/api/network')
def api_network():
    ips = get_local_ips()
    port = request.host.split(':')[-1] if ':' in request.host else '5000'
    urls = [f"http://{ip}:{port}/play" for ip in ips]
    return jsonify({
        "ips": ips,
        "port": port,
        "urls": urls,
        "primary_url": urls[0] if urls else f"http://localhost:{port}/play"
    })

@app.route('/api/games')
def api_games():
    return jsonify(game_mgr.get_available_games())

# --- Socket.IO Event Handlers ---

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('join_host')
def handle_join_host():
    join_room('host_room')
    game_mgr.set_host_sid(request.sid)
    try:
        state = game_mgr.get_host_state()
        emit('host_update', state)
    except Exception as e:
        import traceback
        traceback.print_exc()
        emit('error_message', {'message': f'Server error: {e}'})

@socketio.on('select_game')
def handle_select_game(data):
    game_id = data.get('game_id', 'fibbage')
    options = data.get('options', {})
    game_mgr.select_game(game_id, options)
    broadcast_game_update()

@socketio.on('return_to_hub')
def handle_return_to_hub():
    game_mgr.return_to_hub()
    broadcast_game_update()

@socketio.on('restart_session')
def handle_restart_session(data=None):
    reset_scores = (data or {}).get('reset_scores', False) if isinstance(data, dict) else False
    game_mgr.restart_session(reset_scores=reset_scores)
    broadcast_game_update()

@socketio.on('start_game')
def handle_start_game():
    success = game_mgr.start_game()
    if success:
        broadcast_game_update()
    else:
        emit('error_message', {'message': 'Need at least 1 player to start!'}, room=request.sid)

@socketio.on('host_advance')
def handle_host_advance():
    game_mgr.advance_phase()
    broadcast_game_update()

@socketio.on('join_player')
def handle_join_player(data):
    join_room('players_room')
    player_id = data.get('player_id')
    name = data.get('name', 'Player')
    avatar = data.get('avatar')
    is_local = data.get('is_local', False)
    
    if not player_id:
        player_id = f"p_{request.sid[:8]}"
        
    pdata = game_mgr.join_player(player_id, name, avatar, sid=request.sid, is_local=is_local)
    
    # Send tailored state back to this player
    emit('player_update', game_mgr.get_player_state(player_id), room=request.sid)
    # Broadcast updated player list to host
    socketio.emit('host_update', game_mgr.get_host_state(), room='host_room')

@socketio.on('get_player_state')
def handle_get_player_state(data):
    player_id = data.get('player_id')
    if player_id:
        emit('player_update', game_mgr.get_player_state(player_id), room=request.sid)

@socketio.on('player_action')
def handle_player_action(data):
    player_id = data.get('player_id')
    action = data.get('action')
    payload = data.get('data', {})
    
    if player_id and action:
        changed = game_mgr.handle_player_action(player_id, action, payload)
        if changed:
            broadcast_game_update()
        else:
            # Refresh this player's view
            emit('player_update', game_mgr.get_player_state(player_id), room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    # Sockets can reconnect; player profiles are kept so virtual players and phone players keep scores
    pass

if __name__ == '__main__':
    local_ips = get_local_ips()
    print("=" * 60)
    print("PARTY GAMES HUB SERVER STARTED")
    print(f"Host Screen URL:   http://localhost:5000/host")
    for ip in local_ips:
        print(f"Phone Join URL:   http://{ip}:5000/play")
    print("=" * 60)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
