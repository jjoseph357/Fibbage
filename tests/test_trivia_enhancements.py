import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from games.trivia.trivia_game import TriviaGame
from games.trivia.questions import TRIVIA_QUESTIONS, get_random_trivia_questions

class TestTriviaEnhancements(unittest.TestCase):

    def setUp(self):
        self.players = {
            "p1": {"name": "Alice", "avatar": "🦊", "score": 0},
            "p2": {"name": "Bob", "avatar": "🐼", "score": 0},
            "p3": {"name": "Charlie", "avatar": "🐸", "score": 0}
        }

    def test_deck_contains_diverse_types(self):
        types = {q["type"] for q in TRIVIA_QUESTIONS}
        self.assertIn("multiple_choice", types)
        self.assertIn("slider", types)
        self.assertIn("multi_select", types)
        self.assertIn("true_false", types)
        self.assertGreaterEqual(len(TRIVIA_QUESTIONS), 30)

    def test_slider_question_grading(self):
        game = TriviaGame("GAME", self.players, {"rounds": 1, "timer": 30})
        # Force a slider question
        game.current_q = {
            "type": "slider",
            "question": "Titanic sink year?",
            "category": "History",
            "min": 1900,
            "max": 1930,
            "step": 1,
            "unit": "",
            "answer": 1912
        }
        game.stage = "answering"

        # P1: Exact match (1912) -> Bullseye 1000 pts
        # P2: Close match (1913, diff 1 in 30 = 3.3%) -> 800 pts
        # P3: Distant match (1900, diff 12 in 30 = 40%) -> 0 pts
        game.handle_player_action("p1", "submit_answer", {"choice": 1912})
        game.handle_player_action("p2", "submit_answer", {"choice": 1913})
        game.handle_player_action("p3", "submit_answer", {"choice": 1900})

        # Advance to reveal
        self.assertEqual(game.stage, "reveal")
        self.assertGreaterEqual(game.round_score_deltas["p1"], 1000)
        self.assertGreaterEqual(game.round_score_deltas["p2"], 800)
        self.assertEqual(game.round_score_deltas["p3"], 0)

        # Host view structure
        host_view = game.get_host_view()
        self.assertEqual(host_view["q_type"], "slider")
        self.assertEqual(len(host_view["slider_guesses"]), 3)
        self.assertEqual(host_view["slider_guesses"][0]["id"], "p1")

    def test_multiselect_question_grading(self):
        game = TriviaGame("GAME", self.players, {"rounds": 1, "timer": 30})
        # Force a multi_select question
        game.current_q = {
            "type": "multi_select",
            "question": "Select egg laying mammals:",
            "category": "Biology",
            "options": ["Platypus", "Echidna", "Kangaroo", "Koala"],
            "answer": ["Platypus", "Echidna"]
        }
        game.stage = "answering"

        # P1: Perfect (Platypus, Echidna) -> Full points
        # P2: Partial (Platypus only) -> Partial points
        # P3: Wrong (Kangaroo, Koala) -> 0 points
        game.handle_player_action("p1", "submit_answer", {"choice": ["Platypus", "Echidna"]})
        game.handle_player_action("p2", "submit_answer", {"choice": ["Platypus"]})
        game.handle_player_action("p3", "submit_answer", {"choice": ["Kangaroo", "Koala"]})

        self.assertEqual(game.stage, "reveal")
        self.assertGreaterEqual(game.round_score_deltas["p1"], 750)
        self.assertGreater(game.round_score_deltas["p2"], 0)
        self.assertLess(game.round_score_deltas["p2"], game.round_score_deltas["p1"])
        self.assertEqual(game.round_score_deltas["p3"], 0)

    def test_true_false_question_grading(self):
        game = TriviaGame("GAME", self.players, {"rounds": 1, "timer": 30})
        game.current_q = {
            "type": "true_false",
            "question": "A group of crows is a Murder.",
            "category": "Nature",
            "options": ["True", "False"],
            "answer": "True"
        }
        game.stage = "answering"

        game.handle_player_action("p1", "submit_answer", {"choice": "True"})
        game.handle_player_action("p2", "submit_answer", {"choice": "False"})
        game.handle_player_action("p3", "submit_answer", {"choice": "True"})

        self.assertEqual(game.stage, "reveal")
        self.assertGreaterEqual(game.round_score_deltas["p1"], 500)
        self.assertEqual(game.round_score_deltas["p2"], 0)
        self.assertGreaterEqual(game.round_score_deltas["p3"], 500)

    def test_player_view_contains_timer(self):
        game = TriviaGame("GAME", self.players, {"rounds": 2, "timer": 25})
        game.start()
        p1_view = game.get_player_view("p1")
        self.assertIn("timer", p1_view)
        self.assertEqual(p1_view["timer"], 25)
        self.assertEqual(p1_view["timer_seconds"], 25)

        # Tick 5 seconds
        for _ in range(5):
            game.time_remaining -= 1
        p1_view_updated = game.get_player_view("p1")
        self.assertEqual(p1_view_updated["timer"], 20)

if __name__ == '__main__':
    unittest.main()

