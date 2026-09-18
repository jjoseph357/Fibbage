import unittest
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from games import list_games, get_game_class, GAME_REGISTRY
from games.bible_trivia.bible_trivia_game import BibleTriviaGame
from games.bible_trivia.questions import BIBLE_TRIVIA_QUESTIONS, get_random_bible_trivia_questions
from games.bible_trivia.bible_api import fetch_bible_verses, DEFAULT_COPYRIGHT

class TestBibleTriviaGame(unittest.TestCase):

    def setUp(self):
        self.players = {
            f"p{i+1}": {"name": f"Player {i+1}", "avatar": "👤", "score": 0}
            for i in range(20)
        }

    def test_registry_integration(self):
        games = list_games()
        bible_game = next((g for g in games if g["id"] == "bible_trivia"), None)
        self.assertIsNotNone(bible_game)
        self.assertEqual(bible_game["name"], "Scripture Sprint: Bible Trivia")
        self.assertEqual(get_game_class("bible_trivia"), BibleTriviaGame)
        self.assertIn("bible_trivia", GAME_REGISTRY)

    def test_questions_deck_richness_and_balance(self):
        self.assertGreaterEqual(len(BIBLE_TRIVIA_QUESTIONS), 25)
        types = {q["type"] for q in BIBLE_TRIVIA_QUESTIONS}
        self.assertIn("slider", types)
        self.assertIn("multi_select", types)
        self.assertIn("multiple_choice", types)
        self.assertIn("true_false", types)

        testaments = {q.get("testament") for q in BIBLE_TRIVIA_QUESTIONS}
        self.assertIn("Old Testament", testaments)
        self.assertIn("New Testament", testaments)

        for q in BIBLE_TRIVIA_QUESTIONS:
            self.assertIn("verse_ref", q)
            self.assertIn("question", q)
            self.assertIn("explanation", q)

    def test_bible_api_fetch_and_copyright(self):
        # Verification helper should produce valid data structure and copyright attribution
        res = fetch_bible_verses("Gen. 1:1; John 1:1")
        self.assertIsInstance(res, dict)
        self.assertIn("copyright", res)
        self.assertIn("ref", res)
        self.assertTrue(len(res["copyright"]) > 0)

    def test_slider_scoring(self):
        game = BibleTriviaGame("TEST", {"p1": {"name": "Alice", "avatar": "👑", "score": 0}}, {"rounds": 1, "timer": 30})
        game.current_q = {
            "type": "slider",
            "testament": "Old Testament",
            "category": "Wisdom",
            "question": "Chapters in Psalms?",
            "min": 50,
            "max": 200,
            "step": 5,
            "unit": "psalms",
            "answer": 150,
            "verse_ref": "Psa. 150:1",
            "explanation": "Psalms has 150 chapters."
        }
        game.stage = "answering"
        game.round_start_time = time.time()

        game.handle_player_action("p1", "submit_answer", {"choice": 150})
        self.assertEqual(game.stage, "reveal")
        self.assertGreaterEqual(game.players["p1"]["score"], 1000)

        host_view = game.get_host_view()
        self.assertEqual(host_view["q_type"], "slider")
        self.assertEqual(len(host_view["slider_guesses"]), 1)
        self.assertEqual(host_view["correct_answer"], 150)

    def test_multiselect_scoring(self):
        game = BibleTriviaGame("TEST", {"p1": {"name": "Bob", "avatar": "🛡️", "score": 0}}, {"rounds": 1, "timer": 30})
        game.current_q = {
            "type": "multi_select",
            "testament": "New Testament",
            "category": "Gospels",
            "question": "Select fishermen disciples:",
            "options": ["Peter", "Andrew", "Matthew", "Paul"],
            "shuffled_options": ["Peter", "Andrew", "Matthew", "Paul"],
            "answer": ["Peter", "Andrew"],
            "verse_ref": "Matt. 4:18-20",
            "explanation": "Peter and Andrew were fishermen."
        }
        game.stage = "answering"
        game.round_start_time = time.time()

        game.handle_player_action("p1", "submit_answer", {"choice": ["Peter", "Andrew"]})
        self.assertEqual(game.stage, "reveal")
        self.assertGreaterEqual(game.players["p1"]["score"], 750)

    def test_twenty_players_gameplay(self):
        game = BibleTriviaGame("TEST", self.players, {"rounds": 2, "timer": 30})
        game.current_q = {
            "type": "true_false",
            "testament": "New Testament",
            "category": "Paul",
            "question": "Paul was a Roman citizen by birth.",
            "options": ["True", "False"],
            "shuffled_options": ["True", "False"],
            "answer": "True",
            "verse_ref": "Acts 22:28",
            "explanation": "Paul was born a Roman citizen."
        }
        game.stage = "answering"
        game.round_start_time = time.time()

        for i in range(10):
            pid = f"p{i+1}"
            game.handle_player_action(pid, "submit_answer", {"choice": "True"})

        for i in range(10, 20):
            pid = f"p{i+1}"
            game.handle_player_action(pid, "submit_answer", {"choice": "False"})

        self.assertEqual(game.stage, "reveal")
        for i in range(10):
            self.assertGreaterEqual(game.players[f"p{i+1}"]["score"], 500)
        for i in range(10, 20):
            self.assertEqual(game.players[f"p{i+1}"]["score"], 0)

        host_view = game.get_host_view()
        self.assertEqual(len(host_view["leaderboard"]), 20)
        self.assertEqual(host_view["verse_ref"], "Acts 22:28")
        self.assertIn("copyright", host_view)

    def test_question_deck_uniqueness_and_schema(self):
        self.assertGreaterEqual(len(BIBLE_TRIVIA_QUESTIONS), 250)
        seen = set()
        for idx, q in enumerate(BIBLE_TRIVIA_QUESTIONS):
            text = q["question"].strip().lower()
            self.assertNotIn(text, seen, f"Duplicate question text found at index {idx}: {q['question']}")
            seen.add(text)

            self.assertIn("type", q)
            self.assertIn("testament", q)
            self.assertIn("category", q)
            self.assertIn("question", q)
            self.assertIn("verse_ref", q)
            self.assertIn("explanation", q)
            self.assertIn("answer", q)

            if q["type"] in ["multiple_choice", "multi_select", "true_false"]:
                self.assertIn("options", q)
                if q["type"] == "multiple_choice":
                    self.assertIn(q["answer"], q["options"])
                elif q["type"] == "multi_select":
                    self.assertIsInstance(q["answer"], list)
                    for ans in q["answer"]:
                        self.assertIn(ans, q["options"])
                elif q["type"] == "true_false":
                    self.assertIn(q["answer"], ["True", "False"])
            elif q["type"] == "slider":
                self.assertIn("min", q)
                self.assertIn("max", q)
                self.assertIn("step", q)
                self.assertIn("unit", q)
                self.assertTrue(q["min"] <= q["answer"] <= q["max"])

    def test_bible_trivia_player_view_contains_timer(self):
        game = BibleTriviaGame("TEST", self.players, {"rounds": 2, "timer": 40})
        game.start()
        p1_view = game.get_player_view("p1")
        self.assertIn("timer", p1_view)
        self.assertEqual(p1_view["timer"], 40)
        self.assertEqual(p1_view["timer_seconds"], 40)

        # Tick timer down
        for _ in range(8):
            game.time_remaining -= 1
        p1_view_updated = game.get_player_view("p1")
        self.assertEqual(p1_view_updated["timer"], 32)

if __name__ == '__main__':
    unittest.main()


