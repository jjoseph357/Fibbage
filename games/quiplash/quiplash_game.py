import random
from typing import Dict, Any, List, Optional
from games.base_game import BaseGame
from games.quiplash.prompts import get_random_quiplash_prompts, load_quiplash_prompts

BACKUP_QUIPS = [
    "I ran out of time, so here's a potato 🥔",
    "Blame my slow typing fingers",
    "Whatever Bob wrote, but slightly worse",
    "A strongly worded email to management",
    "Existential dread and some glitter",
    "A screaming goat in a business suit",
    "Unsolicited financial advice from a toddler",
    "My lawyer advised me not to answer this",
    "Hot dog smoothies for everyone",
    "A completely normal human reaction",
    "Aggressive tap dancing in silence",
    "Just vibes and questionable choices",
    "A raccoon holding a tiny spatula",
    "Pretending I didn't hear the question",
    "Thirty pounds of pure unflavored gelatin",
    "A microwave set to 99:99",
    "Tax fraud, but make it festive",
    "Crying softly into a bowl of dry cereal",
    "An apology letter written in crayon",
    "A pigeon with suspicious confidence",
    "Three raccoons in a trench coat",
    "A suspiciously sticky high five",
    "A very emotional ukulele solo",
    "My browser history would shock you",
    "A cactus that craves affection",
    "An aggressively polite duel to the death",
    "Spicy water and pure chaos",
    "A dramatic pause that lasted 40 minutes",
    "Deep-fried butter on a selfie stick",
    "A glitter bomb addressed to my enemies"
]

class QuiplashGame(BaseGame):
    ID = "quiplash"
    NAME = "Quiplash: Say Anything"
    DESCRIPTION = "Write hilarious punchlines and battle head-to-head for votes!"
    ICON = "💥"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 24
    ESTIMATED_TIME = "10-15m"
    CATEGORY = "Comedy & Battles"

    def __init__(self, room_code: str, players: Dict[str, Dict[str, Any]], options: Optional[Dict[str, Any]] = None):
        super().__init__(room_code, players, options)
        num_players = max(2, len(players))
        used_prompts = (options or {}).get("used_prompts")
        self.prompts_deck = get_random_quiplash_prompts(max(60, num_players * self.total_rounds), used_prompts=used_prompts)
        self.matchups: List[Dict[str, Any]] = [] # [{ prompt, image, p1_id, p2_id, p1_answer, p2_answer, votes: { pid: 'p1'|'p2' } }]
        self.current_matchup_idx = 0
        self.player_submissions: Dict[str, Dict[int, str]] = {} # pid -> { matchup_idx: answer }
        self.round_score_deltas: Dict[str, int] = {pid: 0 for pid in self.players}

    def start(self) -> None:
        self.current_round = 1
        self._start_round()

    def _start_round(self) -> None:
        self.round_score_deltas = {pid: 0 for pid in self.players}
        pids = list(self.players.keys())
        self.matchups = []
        self.player_submissions = {pid: {} for pid in pids}
        self.current_matchup_idx = 0
        
        # Build matchups for this round
        if len(pids) == 2:
            # 2 players: 1 direct showdown
            prompt_data = self._get_next_prompt()
            self.matchups.append({
                "id": 0,
                "prompt": prompt_data["prompt"],
                "image": prompt_data["image"],
                "p1_id": pids[0],
                "p2_id": pids[1],
                "p1_answer": "",
                "p2_answer": "",
                "votes": {},
                "revealed": False
            })
        else:
            # 3+ players: circular pairing so everyone competes in 2 matchups
            random.shuffle(pids)
            n = len(pids)
            for i in range(n):
                p1 = pids[i]
                p2 = pids[(i + 1) % n]
                prompt_data = self._get_next_prompt()
                self.matchups.append({
                    "id": i,
                    "prompt": prompt_data["prompt"],
                    "image": prompt_data["image"],
                    "p1_id": p1,
                    "p2_id": p2,
                    "p1_answer": "",
                    "p2_answer": "",
                    "votes": {},
                    "revealed": False
                })

        self.stage = "answering"
        self.time_remaining = self.timer_seconds

    def _get_next_prompt(self) -> Dict[str, Any]:
        if self.prompts_deck:
            return self.prompts_deck.pop(0)
        return random.choice(load_quiplash_prompts())

    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        if player_id not in self.players:
            return False

        if self.stage == "answering" and action == "submit_quip":
            matchup_id = int(data.get("matchup_id", 0))
            answer = (data.get("answer") or "").strip()
            if not answer:
                return False

            self.player_submissions[player_id][matchup_id] = answer
            
            # Check if this player finished all assigned matchups
            assigned_matchups = [m for m in self.matchups if m["p1_id"] == player_id or m["p2_id"] == player_id]
            if len(self.player_submissions[player_id]) >= len(assigned_matchups):
                pass

            # Check if all matchups across all players are complete
            all_done = True
            for m in self.matchups:
                p1_has = m["id"] in self.player_submissions.get(m["p1_id"], {})
                p2_has = m["id"] in self.player_submissions.get(m["p2_id"], {})
                if not (p1_has and p2_has):
                    all_done = False
                    break
            
            if all_done:
                self.advance_phase()
            return True

        elif self.stage == "battle" and action == "submit_vote":
            choice = data.get("choice") # 'p1' or 'p2'
            if choice not in ['p1', 'p2']:
                return False
            
            cur_m = self.matchups[self.current_matchup_idx]
            # Head-to-head matchup authors cannot vote at all
            if player_id == cur_m["p1_id"] or player_id == cur_m["p2_id"]:
                return False

            cur_m["votes"][player_id] = choice
            
            # Check if all eligible voters voted
            eligible_voters = [pid for pid in self.players if pid != cur_m["p1_id"] and pid != cur_m["p2_id"]]
            if len(eligible_voters) > 0 and len(cur_m["votes"]) >= len(eligible_voters):
                self.advance_phase()
            return True

        return False

    def advance_phase(self) -> bool:
        if self.stage == "answering":
            # Populate answers into matchups
            backup_idx = 0
            for m in self.matchups:
                m["p1_answer"] = self.player_submissions.get(m["p1_id"], {}).get(m["id"]) or BACKUP_QUIPS[backup_idx % len(BACKUP_QUIPS)]
                backup_idx += 1
                m["p2_answer"] = self.player_submissions.get(m["p2_id"], {}).get(m["id"]) or BACKUP_QUIPS[backup_idx % len(BACKUP_QUIPS)]
                backup_idx += 1
                m["votes"] = {}
                m["revealed"] = False

            self.stage = "battle"
            self.current_matchup_idx = 0
            self.time_remaining = self.timer_seconds
            return True

        elif self.stage == "battle":
            cur_m = self.matchups[self.current_matchup_idx]
            if not cur_m["revealed"]:
                # Tally votes for this matchup
                p1_votes = sum(1 for v in cur_m["votes"].values() if v == 'p1')
                p2_votes = sum(1 for v in cur_m["votes"].values() if v == 'p2')
                total_votes = p1_votes + p2_votes

                multiplier = 2 if self.current_round >= self.total_rounds else 1
                
                if total_votes > 0:
                    p1_pct = int((p1_votes / total_votes) * 100)
                    p2_pct = int((p2_votes / total_votes) * 100)
                    
                    p1_pts = p1_pct * 10 * multiplier
                    p2_pts = p2_pct * 10 * multiplier

                    # Quiplash Bonus (100% sweep with at least 2 votes)
                    if p1_votes > 0 and p2_votes == 0 and total_votes >= 2:
                        p1_pts += 500 * multiplier
                    elif p2_votes > 0 and p1_votes == 0 and total_votes >= 2:
                        p2_pts += 500 * multiplier

                    self.round_score_deltas[cur_m["p1_id"]] += p1_pts
                    self.round_score_deltas[cur_m["p2_id"]] += p2_pts
                    self.add_score(cur_m["p1_id"], p1_pts)
                    self.add_score(cur_m["p2_id"], p2_pts)
                else:
                    # In 2-player or no votes, give flat tie points
                    self.round_score_deltas[cur_m["p1_id"]] += 500 * multiplier
                    self.round_score_deltas[cur_m["p2_id"]] += 500 * multiplier
                    self.add_score(cur_m["p1_id"], 500 * multiplier)
                    self.add_score(cur_m["p2_id"], 500 * multiplier)

                cur_m["revealed"] = True
                self.time_remaining = 8
                return True
            else:
                # Move to next matchup or scoreboard
                if self.current_matchup_idx < len(self.matchups) - 1:
                    self.current_matchup_idx += 1
                    self.time_remaining = self.timer_seconds
                    return True
                else:
                    self.stage = "scoreboard"
                    return True

        elif self.stage == "scoreboard":
            if self.current_round < self.total_rounds:
                self.current_round += 1
                self._start_round()
                return True
            else:
                self.stage = "game_over"
                return False

        return False

    def get_host_view(self) -> Dict[str, Any]:
        cur_m = self.matchups[self.current_matchup_idx] if self.matchups else None
        
        matchup_data = None
        if cur_m:
            p1_votes = sum(1 for v in cur_m["votes"].values() if v == 'p1')
            p2_votes = sum(1 for v in cur_m["votes"].values() if v == 'p2')
            total = p1_votes + p2_votes
            p1_pct = int((p1_votes / total) * 100) if total > 0 else 50
            p2_pct = int((p2_votes / total) * 100) if total > 0 else 50
            is_quiplash = (p1_pct == 100 or p2_pct == 100) and total >= 2

            matchup_data = {
                "matchup_index": self.current_matchup_idx + 1,
                "total_matchups": len(self.matchups),
                "prompt": cur_m["prompt"],
                "image": cur_m["image"],
                "p1_name": self.players[cur_m["p1_id"]]["name"] if cur_m["revealed"] else "Player 1",
                "p1_avatar": self.players[cur_m["p1_id"]]["avatar"] if cur_m["revealed"] else "🎭",
                "p1_answer": cur_m["p1_answer"],
                "p1_votes": p1_votes if cur_m["revealed"] else None,
                "p1_pct": p1_pct if cur_m["revealed"] else None,
                "p2_name": self.players[cur_m["p2_id"]]["name"] if cur_m["revealed"] else "Player 2",
                "p2_avatar": self.players[cur_m["p2_id"]]["avatar"] if cur_m["revealed"] else "🎭",
                "p2_answer": cur_m["p2_answer"],
                "p2_votes": p2_votes if cur_m["revealed"] else None,
                "p2_pct": p2_pct if cur_m["revealed"] else None,
                "revealed": cur_m["revealed"],
                "is_quiplash": is_quiplash if cur_m["revealed"] else False,
                "voter_avatars": [
                    {"id": vid, "avatar": self.players[vid]["avatar"], "choice": choice}
                    for vid, choice in cur_m["votes"].items()
                ] if cur_m["revealed"] else []
            }

        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "timer": self.time_remaining,
            "players_status": {
                pid: {
                    "name": pdata["name"],
                    "avatar": pdata["avatar"],
                    "score": pdata["score"],
                    "has_submitted": len(self.player_submissions.get(pid, {})) >= len([m for m in self.matchups if m["p1_id"] == pid or m["p2_id"] == pid]) if self.stage == "answering" else (pid in (cur_m["votes"] if cur_m else {}))
                }
                for pid, pdata in self.players.items()
            },
            "matchup": matchup_data,
            "round_score_deltas": self.round_score_deltas,
            "leaderboard": self.get_leaderboard()
        }

    def get_player_view(self, player_id: str) -> Dict[str, Any]:
        pdata = self.players.get(player_id, {})
        
        # In answering phase, find matchups assigned to this player
        my_prompts = []
        if self.stage == "answering":
            for m in self.matchups:
                if m["p1_id"] == player_id or m["p2_id"] == player_id:
                    my_prompts.append({
                        "matchup_id": m["id"],
                        "prompt": m["prompt"],
                        "image": m["image"],
                        "submitted_answer": self.player_submissions.get(player_id, {}).get(m["id"])
                    })

        # In battle phase, determine if player is voter or participant
        cur_m = self.matchups[self.current_matchup_idx] if self.matchups else None
        is_my_matchup = False
        can_vote = False
        my_vote = None

        if cur_m and self.stage == "battle":
            is_my_matchup = (cur_m["p1_id"] == player_id or cur_m["p2_id"] == player_id)
            can_vote = not is_my_matchup
            my_vote = cur_m["votes"].get(player_id)

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
            "my_prompts": my_prompts,
            "is_my_matchup": is_my_matchup,
            "can_vote": can_vote,
            "my_vote": my_vote,
            "battle_matchup": {
                "prompt": cur_m["prompt"] if cur_m else "",
                "image": cur_m["image"] if cur_m else None,
                "p1_answer": cur_m["p1_answer"] if cur_m else "",
                "p2_answer": cur_m["p2_answer"] if cur_m else "",
                "revealed": cur_m["revealed"] if cur_m else False
            } if cur_m else None,
            "leaderboard": self.get_leaderboard() if self.stage in ["scoreboard", "game_over"] else None
        }
