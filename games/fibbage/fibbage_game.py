import random
from typing import Dict, Any, List, Optional
from games.base_game import BaseGame
from games.fibbage.prompts import get_random_prompts, FIBBAGE_PROMPTS

BACKUP_LIES = [
    "Hot Dog Water", "A Rubber Chicken", "Nicholas Cage", "Secret Cheese",
    "Bubble Wrap", "A Fake Mustache", "A Potted Fern", "Taxidermy Squirrels",
    "Silly Putty", "A Disco Ball", "A Live Possum", "Glitter Cannons",
    "A Bag of Toenails", "A Haunted Toaster", "Expired Yogurt", "A Medieval Broadsword",
    "Pocket Sand", "Crying in the Shower", "A Wet Sock", "A Jar of Mayonnaise",
    "Competitive Kazoo", "Uncooked Spaghetti", "A Slightly Used Toothpick", "Alien DNA",
    "A Collection of Bellybutton Lint", "Emotional Damage", "An Aggressive Goose", "A Single Corn Flake",
    "Quantum Foam", "A Butter Sculpture", "Discount Fireworks", "An Invisible Cape",
    "A Very Angry Hamster", "Extreme Ironing", "A Broken Slinky", "Precooked Bacon"
]

class FibbageGame(BaseGame):
    ID = "fibbage"
    NAME = "Fibbage: The Bluffing Game"
    DESCRIPTION = "Fool your friends with clever lies while sniffing out the truth!"
    ICON = "🤥"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 24
    ESTIMATED_TIME = "10-15m"
    CATEGORY = "Bluffing & Trivia"

    def __init__(self, room_code: str, players: Dict[str, Dict[str, Any]], options: Optional[Dict[str, Any]] = None):
        super().__init__(room_code, players, options)
        used_prompts = (options or {}).get("used_prompts")
        self.prompts_deck = get_random_prompts(self.total_rounds, used_prompts=used_prompts)
        self.current_prompt_idx = 0
        self.current_prompt: Dict[str, Any] = {}
        
        # Round tracking
        self.player_lies: Dict[str, str] = {}         # pid -> lie text
        self.player_votes: Dict[str, str] = {}        # pid -> answer text chosen
        self.shuffled_options: List[Dict[str, Any]] = [] # [{ text, author_id, is_truth, voters: [] }]
        self.reveal_index = 0
        self.round_score_deltas: Dict[str, int] = {}
        self.round_events: List[str] = []

    def start(self) -> None:
        self.current_round = 1
        self._start_round()

    def _start_round(self) -> None:
        if self.current_prompt_idx < len(self.prompts_deck):
            self.current_prompt = self.prompts_deck[self.current_prompt_idx]
        else:
            self.current_prompt = random.choice(FIBBAGE_PROMPTS)
            
        self.stage = "answering"
        self.player_lies = {}
        self.player_votes = {}
        self.shuffled_options = []
        self.reveal_index = 0
        self.round_score_deltas = {pid: 0 for pid in self.players}
        self.round_events = []
        self.time_remaining = self.timer_seconds

    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        if player_id not in self.players:
            return False

        if self.stage == "answering" and action == "submit_lie":
            lie = (data.get("lie") or "").strip()
            if not lie:
                return False
            # Check if player accidentally guessed the exact truth
            truth = self.current_prompt.get("answer", "")
            if lie.lower() == truth.lower():
                return False # Controller will show "That's the truth!"
            self.player_lies[player_id] = lie
            
            # Check if all players submitted
            if len(self.player_lies) >= len(self.players):
                self.advance_phase()
            return True

        elif self.stage == "voting" and action == "submit_vote":
            choice = data.get("choice")
            if not choice:
                return False
            # Prevent player from voting for their own submitted lie
            my_lie = self.player_lies.get(player_id, "")
            if my_lie and str(choice).strip().lower() == str(my_lie).strip().lower():
                return False

            self.player_votes[player_id] = choice
            
            # Check if all players voted
            if len(self.player_votes) >= len(self.players):
                self.advance_phase()
            return True

        return False

    def advance_phase(self) -> bool:
        if self.stage == "answering":
            # Auto-fill missing lies with funny backups
            used_backups = list(BACKUP_LIES)
            random.shuffle(used_backups)
            for pid in self.players:
                if pid not in self.player_lies:
                    self.player_lies[pid] = used_backups.pop() if used_backups else f"Lie from {self.players[pid]['name']}"

            # Prepare voting options
            options = []
            # Add truth
            truth = self.current_prompt["answer"]
            options.append({
                "text": truth,
                "author_id": None,
                "is_truth": True,
                "voters": []
            })
            # Add player lies
            for pid, lie in self.player_lies.items():
                # Avoid exact duplicate choices
                if not any(opt["text"].lower() == lie.lower() for opt in options):
                    options.append({
                        "text": lie,
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
            # Tabulate votes
            truth_points = 1000 if self.current_round < self.total_rounds else 2000
            fool_points = 500 if self.current_round < self.total_rounds else 1000

            for opt in self.shuffled_options:
                opt["voters"] = []

            for pid, vote_text in self.player_votes.items():
                for opt in self.shuffled_options:
                    if opt["text"].lower() == vote_text.lower():
                        opt["voters"].append(pid)
                        if opt["is_truth"]:
                            # Player found the truth!
                            self.round_score_deltas[pid] += truth_points
                        else:
                            # Author fooled this player!
                            author = opt["author_id"]
                            if author and author != pid:
                                self.round_score_deltas[author] += fool_points
                        break

            # Apply score deltas
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
                self.current_prompt_idx += 1
                self._start_round()
                return True
            else:
                self.stage = "game_over"
                return False

        return False

    def get_host_view(self) -> Dict[str, Any]:
        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "prompt": self.current_prompt.get("prompt", ""),
            "prompt_image": self.current_prompt.get("image", None),
            "timer": self.time_remaining,
            "players_status": {
                pid: {
                    "name": pdata["name"],
                    "avatar": pdata["avatar"],
                    "score": pdata["score"],
                    "has_submitted": pid in self.player_lies if self.stage == "answering" else pid in self.player_votes
                }
                for pid, pdata in self.players.items()
            },
            "options": [
                {
                    "text": opt["text"],
                    "author_id": opt["author_id"] if self.stage in ["reveal", "scoreboard", "game_over"] else None,
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
            "round_score_deltas": self.round_score_deltas,
            "leaderboard": self.get_leaderboard()
        }

    def get_player_view(self, player_id: str) -> Dict[str, Any]:
        pdata = self.players.get(player_id, {})
        my_lie = self.player_lies.get(player_id)
        
        # Options for player in voting phase (disable their own lie)
        filtered_options = []
        if self.stage == "voting":
            for opt in self.shuffled_options:
                is_mine = (opt.get("author_id") == player_id)
                filtered_options.append({
                    "text": opt["text"],
                    "is_own": is_mine
                })

        return {
            "game_id": self.ID,
            "stage": self.stage,
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "timer": self.time_remaining,
            "timer_seconds": self.timer_seconds,
            "prompt": self.current_prompt.get("prompt", ""),
            "prompt_image": self.current_prompt.get("image", None),
            "my_name": pdata.get("name", ""),
            "my_avatar": pdata.get("avatar", "👤"),
            "my_score": pdata.get("score", 0),
            "my_score_delta": self.round_score_deltas.get(player_id, 0),
            "has_submitted": player_id in self.player_lies if self.stage == "answering" else player_id in self.player_votes,
            "my_lie": my_lie,
            "my_vote": self.player_votes.get(player_id),
            "truth": self.current_prompt.get("answer", "") if self.stage in ["reveal", "scoreboard", "game_over"] else None,
            "options": filtered_options,
            "leaderboard": self.get_leaderboard() if self.stage in ["scoreboard", "game_over"] else None
        }
