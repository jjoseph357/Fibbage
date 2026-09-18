import unittest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game_manager import GameManager
from games.fibbage import FibbageGame
from app import app, socketio, timer_running, game_mgr

class TestTimerPlayerSync(unittest.TestCase):

    def setUp(self):
        game_mgr.players.clear()
        game_mgr.return_to_hub()

    def test_tick_timer_does_not_advance_until_zero(self):
        players = {
            "p1": {"name": "Alice", "avatar": "🦊", "score": 0},
            "p2": {"name": "Bob", "avatar": "🐼", "score": 0}
        }
        game_mgr = GameManager("SYNC")
        game_mgr.players = players
        game_mgr.select_game("fibbage", {"rounds": 2, "timer": 15})
        self.assertTrue(game_mgr.start_game())

        self.assertEqual(game_mgr.active_game.time_remaining, 15)
        self.assertEqual(game_mgr.active_game.stage, "answering")

        # Tick 1 second: time decreases to 14, advanced must be False
        advanced = game_mgr.tick_timer()
        self.assertFalse(advanced)
        self.assertEqual(game_mgr.active_game.time_remaining, 14)
        self.assertEqual(game_mgr.active_game.stage, "answering")

        # Set time to 1 second
        game_mgr.active_game.time_remaining = 1
        # Tick: time reaches 0, auto-advances to voting, advanced must be True
        advanced = game_mgr.tick_timer()
        self.assertTrue(advanced)
        self.assertEqual(game_mgr.active_game.stage, "voting")

    def test_timer_loop_does_not_spam_sync_request_to_players(self):
        # Connect host and player clients
        host_client = socketio.test_client(app)
        host_client.emit('join_host')

        player_client = socketio.test_client(app)
        player_client.emit('join_player', {
            'player_id': 'p_sync_test',
            'name': 'SyncTester',
            'avatar': '🦊'
        })

        # Drain initial join messages
        host_client.get_received()
        player_client.get_received()

        # Start a game
        host_client.emit('select_game', {'game_id': 'fibbage', 'options': {'rounds': 2, 'timer': 40}})
        host_client.emit('start_game')

        # Drain start messages
        host_client.get_received()
        player_client.get_received()

        # Let timer tick for 1.5 seconds
        time.sleep(1.5)

        # Host SHOULD receive host_update with updated timer
        host_msgs = host_client.get_received()
        has_host_update = any(m['name'] == 'host_update' for m in host_msgs)
        self.assertTrue(has_host_update)

        # Player SHOULD NOT receive sync_request on every second when phase has not advanced
        player_msgs = player_client.get_received()
        sync_requests = [m for m in player_msgs if m['name'] == 'sync_request']
        self.assertEqual(len(sync_requests), 0, "Players should not receive sync_request on normal timer ticks!")

if __name__ == '__main__':
    unittest.main()
