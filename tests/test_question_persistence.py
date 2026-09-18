import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game_manager import GameManager
from games.fibbage.prompts import get_random_prompts, FIBBAGE_PROMPTS
from games.quiplash.prompts import get_random_quiplash_prompts, load_quiplash_prompts
from games.trivia.questions import get_random_trivia_questions, TRIVIA_QUESTIONS
from games.bible_trivia.questions import get_random_bible_trivia_questions, BIBLE_TRIVIA_QUESTIONS
from games.doodler.words import get_random_doodle_prompts, DOODLE_PROMPTS

class TestQuestionPersistence(unittest.TestCase):

    def test_fibbage_prompt_persistence_and_cycle(self):
        used = set()
        total_prompts = len(FIBBAGE_PROMPTS)
        batch1 = get_random_prompts(5, used_prompts=used)
        self.assertEqual(len(batch1), 5)
        self.assertEqual(len(used), 5)

        batch2 = get_random_prompts(5, used_prompts=used)
        self.assertEqual(len(batch2), 5)
        self.assertEqual(len(used), 10)

        # Ensure no overlap between batch 1 and batch 2
        b1_prompts = {p["prompt"] for p in batch1}
        b2_prompts = {p["prompt"] for p in batch2}
        self.assertEqual(len(b1_prompts.intersection(b2_prompts)), 0)

        # Pull almost entire pool
        remaining = total_prompts - 10
        batch3 = get_random_prompts(remaining, used_prompts=used)
        self.assertEqual(len(used), total_prompts)

        # Exhaustion cycle test: next batch should cleanly reset used and pull fresh
        batch4 = get_random_prompts(5, used_prompts=used)
        self.assertEqual(len(batch4), 5)
        self.assertEqual(len(used), 5)

    def test_trivia_question_persistence_and_cycle(self):
        used = set()
        total_questions = len(TRIVIA_QUESTIONS)
        batch1 = get_random_trivia_questions(6, used_prompts=used)
        batch2 = get_random_trivia_questions(6, used_prompts=used)

        b1_q = {q["question"] for q in batch1}
        b2_q = {q["question"] for q in batch2}
        self.assertEqual(len(b1_q.intersection(b2_q)), 0)
        self.assertEqual(len(used), 12)

    def test_bible_trivia_question_persistence_and_cycle(self):
        used = set()
        batch1 = get_random_bible_trivia_questions(10, used_prompts=used)
        batch2 = get_random_bible_trivia_questions(10, used_prompts=used)

        b1_q = {q["question"] for q in batch1}
        b2_q = {q["question"] for q in batch2}
        self.assertEqual(len(b1_q.intersection(b2_q)), 0)
        self.assertEqual(len(used), 20)

    def test_quiplash_prompt_persistence(self):
        used = set()
        batch1 = get_random_quiplash_prompts(8, used_prompts=used)
        batch2 = get_random_quiplash_prompts(8, used_prompts=used)

        b1_p = {p["prompt"] for p in batch1}
        b2_p = {p["prompt"] for p in batch2}
        self.assertEqual(len(b1_p.intersection(b2_p)), 0)
        self.assertEqual(len(used), 16)

    def test_doodler_prompt_persistence(self):
        used = set()
        batch1 = get_random_doodle_prompts(5, used_prompts=used)
        batch2 = get_random_doodle_prompts(5, used_prompts=used)

        self.assertEqual(len(set(batch1).intersection(set(batch2))), 0)
        self.assertEqual(len(used), 10)

    def test_game_manager_session_persistence_across_games(self):
        gm = GameManager("TEST")
        gm.join_player("p1", "Alice")
        gm.join_player("p2", "Bob")

        # Select and play Trivia Game 1
        gm.select_game("trivia", {"rounds": 3})
        gm.start_game()
        game1_questions = [q["question"] for q in gm.active_game.question_deck]
        self.assertEqual(len(game1_questions), 3)
        self.assertEqual(len(gm.used_prompts["trivia"]), 3)

        # Select and play Trivia Game 2 in same session
        gm.select_game("trivia", {"rounds": 3})
        gm.start_game()
        game2_questions = [q["question"] for q in gm.active_game.question_deck]
        self.assertEqual(len(game2_questions), 3)
        self.assertEqual(len(gm.used_prompts["trivia"]), 6)

        # Verify no overlap between game 1 and game 2
        overlap = set(game1_questions).intersection(set(game2_questions))
        self.assertEqual(len(overlap), 0)

        # Host restarts session
        gm.restart_session(reset_scores=True)
        self.assertEqual(len(gm.used_prompts), 0)
        self.assertEqual(gm.state, "hub")

if __name__ == '__main__':
    unittest.main()
