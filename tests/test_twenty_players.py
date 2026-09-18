import unittest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game_manager import GameManager, DEFAULT_AVATARS
from core.network import get_local_ips
from games import list_games, get_game_class
from games.fibbage import FibbageGame
from games.quiplash import QuiplashGame
from games.trivia import TriviaGame
from games.doodler import DoodlerGame
from app import app, socketio, game_mgr

class TestTwentyPlayers(unittest.TestCase):

    def setUp(self):
        game_mgr.players.clear()
        game_mgr.return_to_hub()
        self.num_players = 20
        self.players = {
            f"p{i+1}": {
                "name": f"Player_{i+1}",
                "avatar": DEFAULT_AVATARS[i % len(DEFAULT_AVATARS)],
                "score": 0
            }
            for i in range(self.num_players)
        }

    def test_avatar_pool_capacity(self):
        self.assertGreaterEqual(len(DEFAULT_AVATARS), 20)
        mgr = GameManager("TEST")
        for i in range(24):
            p = mgr.join_player(f"p_{i+1}", f"User {i+1}")
            self.assertTrue(p["avatar"])
        self.assertEqual(len(mgr.players), 24)

    def test_fibbage_twenty_players(self):
        game = FibbageGame("GAME", self.players, {"rounds": 2, "timer": 45})
        game.start()

        self.assertEqual(game.stage, "answering")
        self.assertEqual(len(game.players), 20)

        # 1. All 20 players submit unique lies
        for i in range(20):
            pid = f"p{i+1}"
            submitted = game.handle_player_action(pid, "submit_lie", {"lie": f"Creative Lie {i+1}"})
            self.assertTrue(submitted)

        # Answering phase auto-advances to voting when all 20 have submitted
        self.assertEqual(game.stage, "voting")
        self.assertEqual(len(game.shuffled_options), 21) # 20 player lies + 1 truth

        truth_text = game.current_prompt["answer"]

        # 2. Half vote truth, half vote for player 1's lie
        for i in range(10):
            pid = f"p{i+1}"
            voted = game.handle_player_action(pid, "submit_vote", {"choice": truth_text})
            self.assertTrue(voted)

        for i in range(10, 20):
            pid = f"p{i+1}"
            voted = game.handle_player_action(pid, "submit_vote", {"choice": "Creative Lie 1"})
            self.assertTrue(voted)

        # Voting phase auto-advances to reveal
        self.assertEqual(game.stage, "reveal")

        # Player 1 got truth points (1000) + 10 players fooled by Lie 1 (10 * 500 = 5000)
        self.assertEqual(game.players["p1"]["score"], 6000)
        # Players 2-10 got 1000 truth points
        for i in range(1, 10):
            self.assertEqual(game.players[f"p{i+1}"]["score"], 1000)
        # Players 11-20 voted for a lie, so score is 0
        for i in range(10, 20):
            self.assertEqual(game.players[f"p{i+1}"]["score"], 0)

        host_view = game.get_host_view()
        self.assertEqual(len(host_view["leaderboard"]), 20)
        self.assertEqual(host_view["leaderboard"][0]["pid"], "p1")
        self.assertEqual(host_view["leaderboard"][0]["score"], 6000)

        # Player views
        p1_view = game.get_player_view("p1")
        self.assertEqual(p1_view["my_score"], 6000)

    def test_quiplash_twenty_players(self):
        game = QuiplashGame("GAME", self.players, {"rounds": 2, "timer": 45})
        game.start()

        self.assertEqual(game.stage, "answering")
        # 20 players -> circular pairing gives 20 matchups
        self.assertEqual(len(game.matchups), 20)

        # Verify every player is assigned to exactly 2 matchups
        for pid in self.players:
            assigned = [m for m in game.matchups if m["p1_id"] == pid or m["p2_id"] == pid]
            self.assertEqual(len(assigned), 2)

        # All 20 players submit their 2 assigned quips
        for pid in self.players:
            p_view = game.get_player_view(pid)
            self.assertEqual(len(p_view["my_prompts"]), 2)
            for item in p_view["my_prompts"]:
                mid = item["matchup_id"]
                submitted = game.handle_player_action(pid, "submit_quip", {
                    "matchup_id": mid,
                    "answer": f"Quip from {pid} on matchup {mid}"
                })
                self.assertTrue(submitted)

        # All submissions received -> auto-advances to battle phase
        self.assertEqual(game.stage, "battle")
        self.assertEqual(game.current_matchup_idx, 0)

        # Matchup 0: p1 vs p2 (18 other players are eligible voters)
        cur_m = game.matchups[0]
        eligible_voters = [pid for pid in self.players if pid != cur_m["p1_id"] and pid != cur_m["p2_id"]]
        self.assertEqual(len(eligible_voters), 18)

        # Authors cannot vote in their own matchup in 3+ player games
        self.assertFalse(game.handle_player_action(cur_m["p1_id"], "submit_vote", {"choice": "p1"}))
        self.assertFalse(game.handle_player_action(cur_m["p2_id"], "submit_vote", {"choice": "p2"}))

        # All 18 eligible voters vote for p1 -> Quiplash 100% sweep bonus!
        for vpid in eligible_voters:
            voted = game.handle_player_action(vpid, "submit_vote", {"choice": "p1"})
            self.assertTrue(voted)

        # Auto-revealed after all eligible voters cast votes
        self.assertTrue(cur_m["revealed"])
        # p1 got 100% (1000 pts) + 500 Quiplash sweep bonus = 1500 pts
        self.assertEqual(game.players[cur_m["p1_id"]]["score"], 1500)
        self.assertEqual(game.players[cur_m["p2_id"]]["score"], 0)

        host_view = game.get_host_view()
        self.assertEqual(len(host_view["leaderboard"]), 20)

    def test_trivia_twenty_players(self):
        game = TriviaGame("GAME", self.players, {"rounds": 3, "timer": 30})
        game.current_q = {
            "type": "multiple_choice",
            "question": "What is 2 + 2?",
            "category": "Math",
            "options": ["4", "3", "5", "6"],
            "shuffled_options": ["4", "3", "5", "6"],
            "answer": "4"
        }
        game.stage = "answering"
        game.round_start_time = time.time()

        correct = "4"
        wrong = "3"

        # First 10 players answer correctly, other 10 answer incorrectly
        for i in range(10):
            pid = f"p{i+1}"
            answered = game.handle_player_action(pid, "submit_answer", {"choice": correct})
            self.assertTrue(answered)

        for i in range(10, 20):
            pid = f"p{i+1}"
            answered = game.handle_player_action(pid, "submit_answer", {"choice": wrong})
            self.assertTrue(answered)

        # Auto-advances to reveal
        self.assertEqual(game.stage, "reveal")
        for i in range(10):
            self.assertGreaterEqual(game.players[f"p{i+1}"]["score"], 500)
        for i in range(10, 20):
            self.assertEqual(game.players[f"p{i+1}"]["score"], 0)

        host_view = game.get_host_view()
        self.assertEqual(len(host_view["leaderboard"]), 20)

    def test_doodler_twenty_players(self):
        game = DoodlerGame("GAME", self.players, {"rounds": 2, "timer": 45})
        game.start()

        self.assertEqual(game.stage, "drawing")
        artist_id = game.current_artist_id

        # Artist submits drawing
        drawn = game.handle_player_action(artist_id, "submit_drawing", {
            "drawing": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        })
        self.assertTrue(drawn)
        self.assertEqual(game.stage, "bluffing")

        # 19 guessers submit bluffs
        guessers = [pid for pid in self.players if pid != artist_id]
        self.assertEqual(len(guessers), 19)

        for i, gpid in enumerate(guessers):
            bluffed = game.handle_player_action(gpid, "submit_bluff", {"bluff": f"Bluff Title {i+1}"})
            self.assertTrue(bluffed)

        # Auto-advances to voting
        self.assertEqual(game.stage, "voting")
        self.assertEqual(len(game.shuffled_options), 20) # 1 real prompt + 19 player bluffs

        real_title = game.current_prompt

        # All 19 guessers vote for real title
        for gpid in guessers:
            voted = game.handle_player_action(gpid, "submit_vote", {"choice": real_title})
            self.assertTrue(voted)

        # Auto-advances to reveal
        self.assertEqual(game.stage, "reveal")

        # Artist gets rewarded for players guessing correctly
        self.assertEqual(game.players[artist_id]["score"], 1000)
        # All 19 guessers get 1000 truth points
        for gpid in guessers:
            self.assertEqual(game.players[gpid]["score"], 1000)

        host_view = game.get_host_view()
        self.assertEqual(len(host_view["leaderboard"]), 20)

    def test_doodler_timeout_preserves_draft_drawing(self):
        game = DoodlerGame("GAME", self.players, {"rounds": 1, "timer": 30})
        game.start()
        artist_id = game.current_artist_id
        
        # Verify artist view contains timer
        artist_view = game.get_player_view(artist_id)
        self.assertEqual(artist_view["timer"], 30)

        # Artist draws and syncs draft strokes
        draft_img = "data:image/png;base64,custom_in_progress_sketch_data"
        saved = game.handle_player_action(artist_id, "draft_drawing", {"drawing": draft_img})
        self.assertFalse(saved) # doesn't advance stage
        self.assertEqual(game.stage, "drawing")

        # Time runs out
        advanced = game.advance_phase()
        self.assertTrue(advanced)
        self.assertEqual(game.stage, "bluffing")
        
        # Drawing must be the artist's in-progress sketch, NOT the placeholder
        self.assertEqual(game.current_drawing, draft_img)

    def test_socketio_hub_and_twenty_players(self):
        test_client_host = socketio.test_client(app)
        test_client_host.emit('join_host')
        host_received = test_client_host.get_received()
        self.assertTrue(any(msg['name'] == 'host_update' for msg in host_received))

        # Select Fibbage from Hub
        test_client_host.emit('select_game', {'game_id': 'fibbage', 'options': {'rounds': 2}})
        
        # Connect 20 player sockets
        player_clients = []
        for i in range(20):
            client = socketio.test_client(app)
            client.emit('join_player', {
                'player_id': f'sock_p{i+1}',
                'name': f'Tester {i+1}',
                'avatar': DEFAULT_AVATARS[i % len(DEFAULT_AVATARS)]
            })
            player_clients.append(client)

        # Host checks player count in lobby
        test_client_host.emit('join_host')
        host_msgs = [msg for msg in test_client_host.get_received() if msg['name'] == 'host_update']
        self.assertTrue(len(host_msgs) > 0)
        host_state = host_msgs[-1]['args'][0]
        self.assertEqual(host_state['players_count'], 20)

        # Start game from host
        test_client_host.emit('start_game')

        # Host receives in_game update
        host_msgs = [msg for msg in test_client_host.get_received() if msg['name'] == 'host_update']
        self.assertTrue(len(host_msgs) > 0)
        host_state = host_msgs[-1]['args'][0]
        self.assertEqual(host_state['manager_state'], 'in_game')
        self.assertEqual(host_state['game_state']['stage'], 'answering')

        # Return to hub
        test_client_host.emit('return_to_hub')
        host_msgs = [msg for msg in test_client_host.get_received() if msg['name'] == 'host_update']
        self.assertTrue(len(host_msgs) > 0)
        host_state = host_msgs[-1]['args'][0]
        self.assertEqual(host_state['manager_state'], 'hub')

    def test_fibbage_backup_lies_twenty_players(self):
        # Test 20 players where none submit lies before time expires
        game = FibbageGame("GAME", self.players, {"rounds": 1, "timer": 10})
        game.start()
        self.assertEqual(game.stage, "answering")

        # Advance without player submissions -> should auto-fill backups
        advanced = game.advance_phase()
        self.assertTrue(advanced)
        self.assertEqual(game.stage, "voting")
        # 20 unique backup lies + 1 truth
        self.assertEqual(len(game.shuffled_options), 21)
        # Verify no crash and options have valid text
        for opt in game.shuffled_options:
            self.assertTrue(len(opt["text"]) > 0)

    def test_quiplash_twenty_four_players(self):
        players_24 = {
            f"p{i+1}": {"name": f"P{i+1}", "avatar": "🎭", "score": 0}
            for i in range(24)
        }
        game = QuiplashGame("GAME", players_24, {"rounds": 2, "timer": 30})
        game.start()
        self.assertEqual(len(game.matchups), 24)

        # Advance through answering using backups
        game.advance_phase()
        self.assertEqual(game.stage, "battle")

        # Step through all 24 matchups
        for _ in range(24):
            self.assertEqual(game.stage, "battle")
            game.advance_phase() # reveal
            game.advance_phase() # next matchup or scoreboard

        self.assertEqual(game.stage, "scoreboard")
        self.assertEqual(len(game.get_leaderboard()), 24)

    def test_late_join_during_active_game(self):
        mgr = GameManager("TEST")
        mgr.select_game("trivia", {"rounds": 3})
        for i in range(15):
            mgr.join_player(f"p_{i+1}", f"Player {i+1}")
        
        self.assertTrue(mgr.start_game())
        self.assertEqual(mgr.state, "in_game")

        # Player 16 joins late
        late_p = mgr.join_player("p_16", "Late Player")
        self.assertEqual(late_p["score"], 0)
        self.assertIn("p_16", mgr.active_game.players)

        # Player 1 re-connects with existing id and keeps score
        mgr.active_game.players["p_1"]["score"] = 1500
        p1 = mgr.join_player("p_1", "Player 1 Renamed", sid="new_sid_123")
        self.assertEqual(p1["name"], "Player 1 Renamed")
        self.assertEqual(mgr.active_game.players["p_1"]["score"], 1500)

if __name__ == '__main__':
    unittest.main()
