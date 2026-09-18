import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from games.fibbage import FibbageGame
from games.quiplash import QuiplashGame
from games.doodler import DoodlerGame

class TestVotingRestrictions(unittest.TestCase):

    def setUp(self):
        self.players = {
            "p1": {"name": "Alice", "avatar": "🦊", "score": 0},
            "p2": {"name": "Bob", "avatar": "🐼", "score": 0},
            "p3": {"name": "Charlie", "avatar": "🐸", "score": 0},
            "p4": {"name": "Diana", "avatar": "🦄", "score": 0}
        }

    def test_fibbage_cannot_vote_for_own_lie(self):
        game = FibbageGame("TEST", self.players, {"rounds": 1, "timer": 30})
        game.current_prompt = {
            "prompt": "In 1900, Hawaii made it illegal to ___.",
            "answer": "Wear fake mustaches",
            "category": "History"
        }
        game.stage = "answering"

        # Submit lies
        game.handle_player_action("p1", "submit_lie", {"lie": "Eat bananas on Sunday"})
        game.handle_player_action("p2", "submit_lie", {"lie": "Ride turtles"})
        game.handle_player_action("p3", "submit_lie", {"lie": "Sing off-key"})
        game.handle_player_action("p4", "submit_lie", {"lie": "Wear hats indoors"})

        self.assertEqual(game.stage, "voting")

        # p1 attempts to vote for their own lie ("Eat bananas on Sunday") -> MUST FAIL
        voted_own = game.handle_player_action("p1", "submit_vote", {"choice": "Eat bananas on Sunday"})
        self.assertFalse(voted_own)
        self.assertNotIn("p1", game.player_votes)

        # p1 votes for p2's lie or the truth -> MUST SUCCEED
        voted_other = game.handle_player_action("p1", "submit_vote", {"choice": "Ride turtles"})
        self.assertTrue(voted_other)
        self.assertEqual(game.player_votes["p1"], "Ride turtles")

        # Player view has is_own flag
        p1_view = game.get_player_view("p1")
        own_opt = next(opt for opt in p1_view["options"] if opt["text"] == "Eat bananas on Sunday")
        self.assertTrue(own_opt["is_own"])
        other_opt = next(opt for opt in p1_view["options"] if opt["text"] == "Ride turtles")
        self.assertFalse(other_opt["is_own"])

    def test_quiplash_head_to_head_players_cannot_vote(self):
        game = QuiplashGame("TEST", self.players, {"rounds": 1, "timer": 30})
        game.start()

        # Submit answers for all matchups
        for m in game.matchups:
            game.handle_player_action(m["p1_id"], "submit_quip", {"matchup_id": m["id"], "answer": f"Quip from {m['p1_id']}"})
            game.handle_player_action(m["p2_id"], "submit_quip", {"matchup_id": m["id"], "answer": f"Quip from {m['p2_id']}"})

        self.assertEqual(game.stage, "battle")
        cur_m = game.matchups[game.current_matchup_idx]
        p1_id = cur_m["p1_id"]
        p2_id = cur_m["p2_id"]

        # Competitors in head-to-head CANNOT vote
        self.assertFalse(game.handle_player_action(p1_id, "submit_vote", {"choice": "p1"}))
        self.assertFalse(game.handle_player_action(p1_id, "submit_vote", {"choice": "p2"}))
        self.assertFalse(game.handle_player_action(p2_id, "submit_vote", {"choice": "p1"}))
        self.assertFalse(game.handle_player_action(p2_id, "submit_vote", {"choice": "p2"}))

        # Check views
        p1_view = game.get_player_view(p1_id)
        self.assertTrue(p1_view["is_my_matchup"])
        self.assertFalse(p1_view["can_vote"])

        # Non-competitors CAN vote
        audience = [pid for pid in self.players if pid != p1_id and pid != p2_id]
        for voter_id in audience:
            voter_view = game.get_player_view(voter_id)
            self.assertFalse(voter_view["is_my_matchup"])
            self.assertTrue(voter_view["can_vote"])
            self.assertTrue(game.handle_player_action(voter_id, "submit_vote", {"choice": "p1"}))

        self.assertTrue(cur_m["revealed"])

    def test_doodler_cannot_vote_for_own_bluff_and_artist_cannot_vote(self):
        game = DoodlerGame("TEST", self.players, {"rounds": 1, "timer": 45})
        game.start()

        artist_id = game.current_artist_id
        game.handle_player_action(artist_id, "submit_drawing", {"drawing": "data:image/png;base64,sample"})
        self.assertEqual(game.stage, "bluffing")

        guessers = [pid for pid in self.players if pid != artist_id]
        for gpid in guessers:
            game.handle_player_action(gpid, "submit_bluff", {"bluff": f"Bluff from {gpid}"})

        self.assertEqual(game.stage, "voting")

        # Artist cannot vote
        self.assertFalse(game.handle_player_action(artist_id, "submit_vote", {"choice": "Any title"}))

        # Guesser cannot vote for their own bluff
        first_guesser = guessers[0]
        own_bluff = f"Bluff from {first_guesser}"
        self.assertFalse(game.handle_player_action(first_guesser, "submit_vote", {"choice": own_bluff}))

        # Guesser can vote for another bluff or the truth
        other_bluff = f"Bluff from {guessers[1]}"
        self.assertTrue(game.handle_player_action(first_guesser, "submit_vote", {"choice": other_bluff}))

if __name__ == '__main__':
    unittest.main()
