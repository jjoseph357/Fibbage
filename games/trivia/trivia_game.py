import random
import time
from typing import Dict, Any, List, Optional
from games.base_game import BaseGame
from games.trivia.questions import get_random_trivia_questions

class TriviaGame(BaseGame):
    ID = "trivia"
    NAME = "Trivia Dash: High Stakes"
    DESCRIPTION = "Race the clock in rapid-fire trivia across pop culture, science, sliders, and absurd facts!"
    ICON = "⚡"
    MIN_PLAYERS = 1
    MAX_PLAYERS = 24
    ESTIMATED_TIME = "5-10m"
    CATEGORY = "Fast Trivia"

    def __init__(self, room_code: str, players: Dict[str, Dict[str, Any]], options: Optional[Dict[str, Any]] = None):
        super().__init__(room_code, players, options)
        used_prompts = (options or {}).get("used_prompts")
        self.question_deck = get_random_trivia_questions(self.total_rounds, used_prompts=used_prompts)
        self.current_q_idx = 0
        self.current_q: Dict[str, Any] = {}
        self.player_answers: Dict[str, Dict[str, Any]] = {} # pid -> { choice, time_taken }
        self.round_start_time = 0.0
        self.round_score_deltas: Dict[str, int] = {}
        self.streaks: Dict[str, int] = {pid: 0 for pid in self.players}

    def start(self) -> None:
        self.current_round = 1
        self._start_round()

    def _start_round(self) -> None:
        if self.current_q_idx < len(self.question_deck):
            self.current_q = dict(self.question_deck[self.current_q_idx])
        else:
            self.current_q = dict(get_random_trivia_questions(1)[0])

        q_type = self.current_q.get("type", "multiple_choice")
        if q_type in ["multiple_choice", "multi_select"]:
            options = list(self.current_q.get("options", []))
            random.shuffle(options)
            self.current_q["shuffled_options"] = options
        elif q_type == "true_false":
            self.current_q["shuffled_options"] = ["True", "False"]
        else:
            self.current_q["shuffled_options"] = []

        self.stage = "answering"
        self.player_answers = {}
        self.round_score_deltas = {pid: 0 for pid in self.players}
        self.time_remaining = self.timer_seconds
        self.round_start_time = time.time()

    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        if player_id not in self.players:
            return False

        if self.stage == "answering" and action == "submit_answer":
            if player_id in self.player_answers:
                return False

            choice = data.get("choice")
            if choice is None:
                choice = data.get("choices")
            if choice is None:
                return False

            time_taken = max(0.1, time.time() - self.round_start_time)
            self.player_answers[player_id] = {
                "choice": choice,
                "time_taken": time_taken
            }

            if len(self.player_answers) >= len(self.players):
                self.advance_phase()
            return True

        return False

    def advance_phase(self) -> bool:
        if self.stage == "answering":
            q_type = self.current_q.get("type", "multiple_choice")
            correct_answer = self.current_q.get("answer")
            max_speed_bonus = 500

            for pid in self.players:
                ans_data = self.player_answers.get(pid)
                if not ans_data:
                    self.streaks[pid] = 0
                    self.round_score_deltas[pid] = 0
                    continue

                user_choice = ans_data["choice"]
                time_taken = ans_data["time_taken"]
                time_ratio = max(0.0, 1.0 - (time_taken / max(1.0, float(self.timer_seconds))))
                speed_bonus = int(max_speed_bonus * time_ratio)
                streak_bonus = min(500, self.streaks.get(pid, 0) * 100)

                earned_pts = 0
                is_correct = False

                if q_type in ["multiple_choice", "true_false"]:
                    if str(user_choice).strip().lower() == str(correct_answer).strip().lower():
                        is_correct = True
                        earned_pts = 500 + speed_bonus + streak_bonus

                elif q_type == "slider":
                    try:
                        target = float(correct_answer)
                        guess = float(user_choice)
                        span = max(1.0, float(self.current_q.get("max", 100) - self.current_q.get("min", 0)))
                        diff = abs(guess - target)
                        pct_err = diff / span

                        if diff == 0:
                            is_correct = True
                            earned_pts = 1000 + speed_bonus + streak_bonus
                        elif pct_err <= 0.05:
                            is_correct = True
                            earned_pts = 800 + int(speed_bonus * 0.8) + streak_bonus
                        elif pct_err <= 0.15:
                            is_correct = True
                            earned_pts = 500 + int(speed_bonus * 0.5) + streak_bonus
                        elif pct_err <= 0.30:
                            is_correct = False
                            earned_pts = 250
                        else:
                            is_correct = False
                            earned_pts = 0
                    except (ValueError, TypeError):
                        earned_pts = 0
                        is_correct = False

                elif q_type == "multi_select":
                    correct_set = {str(x).strip().lower() for x in (correct_answer if isinstance(correct_answer, list) else [correct_answer])}
                    user_set = {str(x).strip().lower() for x in (user_choice if isinstance(user_choice, list) else [user_choice])}
                    
                    true_pos = len(user_set & correct_set)
                    false_pos = len(user_set - correct_set)
                    all_options = self.current_q.get("options", [])
                    wrong_pool = max(1, len(all_options) - len(correct_set))
                    
                    fraction = max(0.0, (true_pos / max(1, len(correct_set))) - 0.5 * (false_pos / wrong_pool))
                    base_pts = int(fraction * 750)
                    
                    if user_set == correct_set:
                        is_correct = True
                        earned_pts = 750 + speed_bonus + streak_bonus
                    elif base_pts > 0:
                        is_correct = False
                        earned_pts = base_pts
                    else:
                        is_correct = False
                        earned_pts = 0

                if is_correct:
                    self.streaks[pid] = self.streaks.get(pid, 0) + 1
                else:
                    self.streaks[pid] = 0

                self.round_score_deltas[pid] = earned_pts
                self.add_score(pid, earned_pts)

            self.stage = "reveal"
            self.time_remaining = 6
            return True

        elif self.stage == "reveal":
            self.stage = "scoreboard"
            return True

        elif self.stage == "scoreboard":
            if self.current_round < self.total_rounds:
                self.current_round += 1
                self.current_q_idx += 1
                self._start_round()
                return True
            else:
                self.stage = "game_over"
                return False

        return False

    def get_host_view(self) -> Dict[str, Any]:
        q_type = self.current_q.get("type", "multiple_choice")
        options_breakdown = []
        slider_guesses = []

        if self.stage in ["reveal", "scoreboard", "game_over"]:
            if q_type == "slider":
                try:
                    target = float(self.current_q.get("answer", 0))
                except (ValueError, TypeError):
                    target = 0.0

                for pid, ans in self.player_answers.items():
                    try:
                        guess_val = float(ans["choice"])
                    except (ValueError, TypeError):
                        guess_val = target
                    diff = abs(guess_val - target)
                    slider_guesses.append({
                        "id": pid,
                        "name": self.players[pid]["name"],
                        "avatar": self.players[pid]["avatar"],
                        "guess": guess_val,
                        "diff": diff,
                        "score_delta": self.round_score_deltas.get(pid, 0)
                    })
                slider_guesses.sort(key=lambda x: x["diff"])

            elif q_type == "multi_select":
                correct_list = self.current_q.get("answer", [])
                for opt in self.current_q.get("shuffled_options", []):
                    voters = []
                    for pid, ans in self.player_answers.items():
                        choices = ans.get("choice", [])
                        if isinstance(choices, list) and opt in choices:
                            voters.append({"id": pid, "name": self.players[pid]["name"], "avatar": self.players[pid]["avatar"]})
                        elif isinstance(choices, str) and opt == choices:
                            voters.append({"id": pid, "name": self.players[pid]["name"], "avatar": self.players[pid]["avatar"]})
                    options_breakdown.append({
                        "text": opt,
                        "is_correct": (opt in correct_list),
                        "voters": voters
                    })

            else:
                for opt in self.current_q.get("shuffled_options", []):
                    voters = [
                        {"id": pid, "name": self.players[pid]["name"], "avatar": self.players[pid]["avatar"]}
                        for pid, ans in self.player_answers.items()
                        if str(ans["choice"]).strip().lower() == str(opt).strip().lower()
                    ]
                    options_breakdown.append({
                        "text": opt,
                        "is_correct": (str(opt).strip().lower() == str(self.current_q.get("answer", "")).strip().lower()),
                        "voters": voters
                    })

        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "category": self.current_q.get("category", "General"),
            "question": self.current_q.get("question", ""),
            "q_type": q_type,
            "min": self.current_q.get("min"),
            "max": self.current_q.get("max"),
            "step": self.current_q.get("step", 1),
            "unit": self.current_q.get("unit", ""),
            "options": self.current_q.get("shuffled_options", []),
            "options_breakdown": options_breakdown,
            "slider_guesses": slider_guesses,
            "correct_answer": self.current_q.get("answer") if self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "explanation": self.current_q.get("explanation", "") if self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "timer": self.time_remaining,
            "players_status": {
                pid: {
                    "name": pdata["name"],
                    "avatar": pdata["avatar"],
                    "score": pdata["score"],
                    "has_submitted": pid in self.player_answers,
                    "streak": self.streaks.get(pid, 0)
                }
                for pid, pdata in self.players.items()
            },
            "round_score_deltas": self.round_score_deltas,
            "leaderboard": self.get_leaderboard()
        }

    def get_player_view(self, player_id: str) -> Dict[str, Any]:
        pdata = self.players.get(player_id, {})
        my_submission = self.player_answers.get(player_id)
        q_type = self.current_q.get("type", "multiple_choice")
        
        is_correct = None
        if my_submission and self.stage in ["reveal", "scoreboard", "game_over"]:
            user_choice = my_submission["choice"]
            correct_ans = self.current_q.get("answer")
            if q_type in ["multiple_choice", "true_false"]:
                is_correct = (str(user_choice).strip().lower() == str(correct_ans).strip().lower())
            elif q_type == "slider":
                try:
                    span = max(1.0, float(self.current_q.get("max", 100) - self.current_q.get("min", 0)))
                    pct_err = abs(float(user_choice) - float(correct_ans)) / span
                    is_correct = (pct_err <= 0.15)
                except (ValueError, TypeError):
                    is_correct = False
            elif q_type == "multi_select":
                correct_set = {str(x).strip().lower() for x in (correct_ans if isinstance(correct_ans, list) else [correct_ans])}
                user_set = {str(x).strip().lower() for x in (user_choice if isinstance(user_choice, list) else [user_choice])}
                is_correct = (user_set == correct_set)

        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "timer": self.time_remaining,
            "timer_seconds": self.timer_seconds,
            "my_name": pdata.get("name", ""),
            "my_avatar": pdata.get("avatar", "👤"),
            "my_score": pdata.get("score", 0),
            "my_score_delta": self.round_score_deltas.get(player_id, 0),
            "streak": self.streaks.get(player_id, 0),
            "category": self.current_q.get("category", "General"),
            "question": self.current_q.get("question", ""),
            "q_type": q_type,
            "min": self.current_q.get("min"),
            "max": self.current_q.get("max"),
            "step": self.current_q.get("step", 1),
            "unit": self.current_q.get("unit", ""),
            "options": self.current_q.get("shuffled_options", []),
            "my_choice": my_submission["choice"] if my_submission else None,
            "has_submitted": my_submission is not None,
            "correct_answer": self.current_q.get("answer") if self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "is_correct": is_correct,
            "explanation": self.current_q.get("explanation", "") if self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "leaderboard": self.get_leaderboard() if self.stage in ["scoreboard", "game_over"] else None
        }
