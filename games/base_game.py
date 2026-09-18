from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseGame(ABC):
    """
    Abstract base class for all party game implementations.
    """
    
    # Metadata to be defined by subclasses
    ID: str = "base"
    NAME: str = "Base Game"
    DESCRIPTION: str = "Base game description"
    ICON: str = "🎮"
    MIN_PLAYERS: int = 2
    MAX_PLAYERS: int = 24
    ESTIMATED_TIME: str = "10-15m"
    CATEGORY: str = "Party"
    
    def __init__(self, room_code: str, players: Dict[str, Dict[str, Any]], options: Optional[Dict[str, Any]] = None):
        self.room_code = room_code
        # players dict: { player_id: { 'name': str, 'avatar': str, 'score': int, ... } }
        self.players = {pid: dict(pdata, score=0) for pid, pdata in players.items()}
        self.options = options or {}
        self.total_rounds = int(self.options.get('rounds', 3))
        self.timer_seconds = int(self.options.get('timer', 45))
        self.current_round = 0
        self.stage = "init"  # e.g., 'answering', 'voting', 'reveal', 'scoreboard', 'game_over'
        self.phase_data: Dict[str, Any] = {}
        self.time_remaining = self.timer_seconds

    @abstractmethod
    def start(self) -> None:
        """Called when game starts from lobby."""
        pass

    @abstractmethod
    def handle_player_action(self, player_id: str, action: str, data: Dict[str, Any]) -> bool:
        """
        Processes an action sent by a player (e.g. submit lie, vote).
        Returns True if state changed.
        """
        pass

    @abstractmethod
    def advance_phase(self) -> bool:
        """
        Advances the game to the next phase (e.g. when timer expires or host clicks next).
        Returns True if advanced, False if game ended.
        """
        pass

    @abstractmethod
    def get_host_view(self) -> Dict[str, Any]:
        """
        Returns public game state safe for display on Host TV screen.
        """
        pass

    @abstractmethod
    def get_player_view(self, player_id: str) -> Dict[str, Any]:
        """
        Returns private game state tailored for a specific player's controller.
        """
        pass

    def add_score(self, player_id: str, points: int):
        if player_id in self.players:
            self.players[player_id]['score'] = max(0, self.players[player_id].get('score', 0) + points)

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        sorted_players = sorted(
            [dict(pid=pid, **pdata) for pid, pdata in self.players.items()],
            key=lambda x: x.get('score', 0),
            reverse=True
        )
        return sorted_players
