import random
from typing import Dict, Any, List, Optional
from games.base_game import BaseGame
from games.doodler.words import get_random_doodle_prompts, DOODLE_PROMPTS

BACKUP_TITLES = [
    "Modern Art Disaster", "Spaghetti Monster", "Something Expensive",
    "A Potato in Distress", "Nightmare Fuel", "Abstract Chaos",
    "A Very Confused Horse", "My Landlord's Portrait", "A Questionable Decision",
    "Unidentified Flying Garbage", "An Existential Crisis", "Accidental Masterpiece",
    "Breakfast Gone Wrong", "A Cursed Artifact", "An Angry Meatball",
    "The Meaning of Life", "A Suspicious Lump", "Alien Architecture",
    "A Fluffy Menace", "Extreme Geometry", "The Last Biscuit",
    "A Dramatic Turn of Events", "A Soggy Cardboard Box", "My Secret Shame",
    "A Cat Planning Revenge", "Duct Tape Miracle", "A Very Round Bird",
    "The Forbidden Donut", "A Ghost with Issues", "Spicy Triangle"
]

class DoodlerGame(BaseGame):
    ID = "doodler"
    NAME = "Doodle Guess: Draw & Bluff"
    DESCRIPTION = "Draw bizarre prompts on your phone while other players bluff fake titles!"
    ICON = "🎨"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 24
    ESTIMATED_TIME = "10-15m"
    CATEGORY = "Drawing & Bluffing"

    def __init__(self, room_code: str, players: Dict[str, Dict[str, Any]], options: Optional[Dict[str, Any]] = None):
        super().__init__(room_code, players, options)
        num_players = max(2, len(players))
        used_prompts = (options or {}).get("used_prompts")
        self.prompts_deck = get_random_doodle_prompts(max(40, self.total_rounds * num_players * 2), used_prompts=used_prompts)
        self.artist_order = list(self.players.keys())
        random.shuffle(self.artist_order)
        self.current_artist_idx = 0
        
        # Round state
        self.current_artist_id = ""
        self.current_prompt = ""
        self.current_drawing = "" # base64 image or path
        self.player_bluffs: Dict[str, str] = {}
        self.player_votes: Dict[str, str] = {}
        self.shuffled_options: List[Dict[str, Any]] = []
        self.reveal_index = 0
        self.round_score_deltas: Dict[str, int] = {}

    def start(self) -> None:
        self.current_round = 1
        self.current_artist_idx = 0
        self._start_round()

    def _start_round(self) -> None:
        self.current_artist_id = self.artist_order[self.current_artist_idx % len(self.artist_order)]
        self.current_prompt = self.prompts_deck.pop(0) if self.prompts_deck else random.choice(DOODLE_PROMPTS)
        self.current_drawing = ""
        self.player_bluffs = {}
        self.player_votes = {}
        self.shuffled_options = []
        self.reveal_index = 0
        self.round_score_deltas = {pid: 0 for pid in self.players}
        self.stage = "drawing"
        self.time_remaining = self.timer_seconds

    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        if player_id not in self.players:
            return False

        if self.stage == "drawing" and player_id == self.current_artist_id:
            if action == "draft_drawing":
                drawing_data = data.get("drawing", "")
                if drawing_data:
                    self.current_drawing = drawing_data
                return False
            elif action == "submit_drawing":
                drawing_data = data.get("drawing", "")
                if drawing_data:
                    self.current_drawing = drawing_data
                self.stage = "bluffing"
                self.time_remaining = self.timer_seconds
                return True

        elif self.stage == "bluffing" and action == "submit_bluff":
            # Artist doesn't submit a bluff
            if player_id == self.current_artist_id:
                return False
            bluff = (data.get("bluff") or "").strip()
            if not bluff:
                return False
            self.player_bluffs[player_id] = bluff

            # Check if all guessers submitted
            guessers = [pid for pid in self.players if pid != self.current_artist_id]
            if len(self.player_bluffs) >= len(guessers):
                self.advance_phase()
            return True

        elif self.stage == "voting" and action == "submit_vote":
            if player_id == self.current_artist_id:
                return False # Artist doesn't vote
            choice = data.get("choice")
            if not choice:
                return False
            # Prevent player from voting for their own bluff
            my_bluff = self.player_bluffs.get(player_id, "")
            if my_bluff and str(choice).strip().lower() == str(my_bluff).strip().lower():
                return False

            self.player_votes[player_id] = choice

            guessers = [pid for pid in self.players if pid != self.current_artist_id]
            if len(self.player_votes) >= len(guessers):
                self.advance_phase()
            return True

        return False

    def advance_phase(self) -> bool:
        if self.stage == "drawing":
            # If artist ran out of time without submitting, use a placeholder
            if not self.current_drawing:
                self.current_drawing = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='300'><text x='50%' y='50%' text-anchor='middle' fill='%23e94560' font-size='20'>Artist ran out of time!</text></svg>"
            self.stage = "bluffing"
            self.time_remaining = self.timer_seconds
            return True

        elif self.stage == "bluffing":
            # Auto-fill missing bluffs
            guessers = [pid for pid in self.players if pid != self.current_artist_id]
            backup_idx = 0
            for pid in guessers:
                if pid not in self.player_bluffs:
                    self.player_bluffs[pid] = BACKUP_TITLES[backup_idx % len(BACKUP_TITLES)]
                    backup_idx += 1

            # Prepare options
            options = [{
                "text": self.current_prompt,
                "author_id": None,
                "is_truth": True,
                "voters": []
            }]
            for pid, bluff in self.player_bluffs.items():
                if not any(opt["text"].lower() == bluff.lower() for opt in options):
                    options.append({
                        "text": bluff,
                        "author_id": pid,
                        "is_truth": False,
                        "voters": []
                    })

            random.shuffle(options)
            self.shuffled_options = options
            self.stage = "voting"
            self.time_remaining = self.timer_seconds
            return True

        elif self.stage == "voting":
            # Calculate points
            truth_points = 1000
            bluff_points = 500
            artist_reward = 1000

            artist_got_guesses = False
            for pid, vote_text in self.player_votes.items():
                for opt in self.shuffled_options:
                    if opt["text"].lower() == vote_text.lower():
                        opt["voters"].append(pid)
                        if opt["is_truth"]:
                            self.round_score_deltas[pid] += truth_points
                            artist_got_guesses = True
                        else:
                            author = opt["author_id"]
                            if author and author != pid:
                                self.round_score_deltas[author] += bluff_points
                        break

            if artist_got_guesses:
                self.round_score_deltas[self.current_artist_id] += artist_reward

            for pid, delta in self.round_score_deltas.items():
                self.add_score(pid, delta)

            self.stage = "reveal"
            self.reveal_index = 0
            self.time_remaining = 8
            return True

        elif self.stage == "reveal":
            if self.reveal_index < len(self.shuffled_options) - 1:
                self.reveal_index += 1
                return True
            else:
                self.stage = "scoreboard"
                return True

        elif self.stage == "scoreboard":
            if self.current_round < self.total_rounds:
                self.current_round += 1
                self.current_artist_idx += 1
                self._start_round()
                return True
            else:
                self.stage = "game_over"
                return False

        return False

    def get_host_view(self) -> Dict[str, Any]:
        artist = self.players.get(self.current_artist_id, {})
        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "artist_name": artist.get("name", "Unknown"),
            "artist_avatar": artist.get("avatar", "🎨"),
            "drawing": self.current_drawing,
            "timer": self.time_remaining,
            "prompt": self.current_prompt if self.stage in ["reveal", "scoreboard", "game_over"] else "???",
            "options": [
                {
                    "text": opt["text"],
                    "author_name": self.players[opt["author_id"]]["name"] if opt["author_id"] and self.stage in ["reveal", "scoreboard", "game_over"] else None,
                    "is_truth": opt["is_truth"] if self.stage in ["reveal", "scoreboard", "game_over"] else None,
                    "voters": [
                        {"id": vid, "name": self.players[vid]["name"], "avatar": self.players[vid]["avatar"]}
                        for vid in opt["voters"]
                    ] if self.stage in ["reveal", "scoreboard", "game_over"] else []
                }
                for opt in self.shuffled_options
            ] if self.stage in ["voting", "reveal", "scoreboard", "game_over"] else [],
            "reveal_index": self.reveal_index,
            "players_status": {
                pid: {
                    "name": pdata["name"],
                    "avatar": pdata["avatar"],
                    "score": pdata["score"],
                    "is_artist": (pid == self.current_artist_id),
                    "has_submitted": bool(self.current_drawing) if pid == self.current_artist_id and self.stage == "drawing" else (pid in self.player_bluffs if self.stage == "bluffing" else pid in self.player_votes)
                }
                for pid, pdata in self.players.items()
            },
            "round_score_deltas": self.round_score_deltas,
            "leaderboard": self.get_leaderboard()
        }

    def get_player_view(self, player_id: str) -> Dict[str, Any]:
        pdata = self.players.get(player_id, {})
        is_artist = (player_id == self.current_artist_id)
        
        filtered_options = []
        if self.stage == "voting" and not is_artist:
            for opt in self.shuffled_options:
                filtered_options.append({
                    "text": opt["text"],
                    "is_own": (opt.get("author_id") == player_id)
                })

        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "my_name": pdata.get("name", ""),
            "my_avatar": pdata.get("avatar", "👤"),
            "my_score": pdata.get("score", 0),
            "my_score_delta": self.round_score_deltas.get(player_id, 0),
            "is_artist": is_artist,
            "artist_name": self.players.get(self.current_artist_id, {}).get("name", ""),
            "artist_avatar": self.players.get(self.current_artist_id, {}).get("avatar", "🎨"),
            "prompt": self.current_prompt if is_artist or self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "drawing": self.current_drawing,
            "timer": self.time_remaining,
            "timer_seconds": self.timer_seconds,
            "has_submitted": bool(self.current_drawing) if is_artist and self.stage == "drawing" else (player_id in self.player_bluffs if self.stage == "bluffing" else player_id in self.player_votes),
            "my_bluff": self.player_bluffs.get(player_id),
            "my_vote": self.player_votes.get(player_id),
            "options": filtered_options,
            "leaderboard": self.get_leaderboard() if self.stage in ["scoreboard", "game_over"] else None
        }
