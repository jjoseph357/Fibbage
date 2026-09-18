import time
from typing import Dict, Any, Optional, List
from games import list_games, get_game_class
from games.base_game import BaseGame

DEFAULT_AVATARS = [
    "🦊", "🐼", "🐸", "🦁", "🦄", "🐙", "🐨", "🐯",
    "🐵", "🐧", "🦉", "🐲", "🤖", "👻", "🚀", "🦖",
    "🦩", "🦔", "🐬", "🦥", "🐱", "🐶", "🐮", "🐷",
    "🐻", "🐰", "🦆", "🦚", "🦋", "🍄", "🌮", "🍕"
]

class GameManager:
    def __init__(self, room_code: str = "GAME"):
        self.room_code = room_code.upper()
        self.state = "hub"  # 'hub', 'lobby', 'in_game'
        self.selected_game_id = "fibbage"
        self.game_options: Dict[str, Any] = {"rounds": 3, "timer": 45}
        self.players: Dict[str, Dict[str, Any]] = {} # pid -> { name, avatar, score, sid, is_local }
        self.active_game: Optional[BaseGame] = None
        self.host_sid: Optional[str] = None
        self.avatar_pool = list(DEFAULT_AVATARS)
        self.used_prompts: Dict[str, set] = {} # game_id -> set of used question/prompt texts

    def set_host_sid(self, sid: str) -> None:
        self.host_sid = sid

    def get_available_games(self) -> List[Dict[str, Any]]:
        return list_games()

    def restart_session(self, reset_scores: bool = False) -> None:
        """Resets session prompt tracking and returns to hub. Clears question history across all games."""
        self.used_prompts.clear()
        self.active_game = None
        self.state = "hub"
        if reset_scores:
            for p in self.players.values():
                p["score"] = 0

    def select_game(self, game_id: str, options: Optional[Dict[str, Any]] = None) -> None:
        self.selected_game_id = game_id
        if options:
            self.game_options.update(options)
        self.state = "lobby"
        self.active_game = None

    def return_to_hub(self) -> None:
        self.state = "hub"
        self.active_game = None

    def join_player(self, player_id: str, name: str, avatar: Optional[str] = None, sid: Optional[str] = None, is_local: bool = False) -> Dict[str, Any]:
        name = (name or "Player").strip()[:16]
        if not avatar:
            avatar = self.avatar_pool[len(self.players) % len(self.avatar_pool)]
            
        if player_id in self.players:
            # Update existing player info
            self.players[player_id]["name"] = name
            if avatar:
                self.players[player_id]["avatar"] = avatar
            if sid:
                self.players[player_id]["sid"] = sid
        else:
            self.players[player_id] = {
                "id": player_id,
                "name": name,
                "avatar": avatar,
                "score": 0,
                "sid": sid,
                "is_local": is_local,
                "joined_at": time.time()
            }

        # If game is in progress and new player joins late, add to active_game players dictionary
        if self.active_game and player_id not in self.active_game.players:
            self.active_game.players[player_id] = {
                "name": name,
                "avatar": avatar,
                "score": 0
            }

        return self.players[player_id]

    def remove_player(self, player_id: str) -> None:
        if player_id in self.players:
            del self.players[player_id]
        if self.active_game and player_id in self.active_game.players:
            del self.active_game.players[player_id]

    def start_game(self) -> bool:
        if len(self.players) < 1:
            return False

        game_cls = get_game_class(self.selected_game_id)
        current_used = self.used_prompts.setdefault(self.selected_game_id, set())
        options = {**self.game_options, "used_prompts": current_used}
        self.active_game = game_cls(self.room_code, self.players, options)
        self.active_game.start()
        self.state = "in_game"
        return True

    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        if self.active_game and self.state == "in_game":
            return self.active_game.handle_player_action(player_id, action, data)
        return False

    def advance_phase(self) -> bool:
        if self.active_game and self.state == "in_game":
            result = self.active_game.advance_phase()
            if self.active_game.stage == "game_over":
                # Keep in_game so podium is shown; host can return to hub or restart
                pass
            return result
        return False

    def tick_timer(self) -> bool:
        """Called periodically (e.g. once per second). Returns True if phase auto-advanced."""
        if self.active_game and self.state == "in_game":
            if self.active_game.time_remaining > 0:
                self.active_game.time_remaining -= 1
                if self.active_game.time_remaining == 0:
                    return self.advance_phase()
        return False

    def get_host_state(self) -> Dict[str, Any]:
        game_meta = next((g for g in list_games() if g["id"] == self.selected_game_id), None)
        base = {
            "room_code": self.room_code,
            "manager_state": self.state,
            "selected_game": game_meta,
            "available_games": list_games(),
            "game_options": self.game_options,
            "players": [{**pdata, 'id': pid} for pid, pdata in self.players.items()],
            "players_count": len(self.players)
        }

        if self.state == "in_game" and self.active_game:
            base["game_state"] = self.active_game.get_host_view()
        else:
            base["game_state"] = None

        return base

    def get_player_state(self, player_id: str) -> Dict[str, Any]:
        pdata = self.players.get(player_id, {})
        base = {
            "room_code": self.room_code,
            "manager_state": self.state,
            "selected_game_id": self.selected_game_id,
            "player_id": player_id,
            "player_name": pdata.get("name", "Spectator"),
            "player_avatar": pdata.get("avatar", "👤"),
            "player_score": pdata.get("score", 0),
            "players_count": len(self.players)
        }

        if self.state == "in_game" and self.active_game:
            base["game_state"] = self.active_game.get_player_view(player_id)
        else:
            base["game_state"] = None

        return base
