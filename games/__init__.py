from typing import Dict, Any, List, Type
from games.base_game import BaseGame
from games.fibbage import FibbageGame
from games.quiplash import QuiplashGame
from games.trivia import TriviaGame
from games.doodler import DoodlerGame
from games.bible_trivia import BibleTriviaGame

GAME_REGISTRY: Dict[str, Type[BaseGame]] = {
    FibbageGame.ID: FibbageGame,
    QuiplashGame.ID: QuiplashGame,
    TriviaGame.ID: TriviaGame,
    BibleTriviaGame.ID: BibleTriviaGame,
    DoodlerGame.ID: DoodlerGame,
}

def list_games() -> List[Dict[str, Any]]:
    """Returns metadata for all available games in the hub."""
    games_meta = []
    for gid, game_cls in GAME_REGISTRY.items():
        games_meta.append({
            "id": game_cls.ID,
            "name": game_cls.NAME,
            "description": game_cls.DESCRIPTION,
            "icon": game_cls.ICON,
            "min_players": game_cls.MIN_PLAYERS,
            "max_players": game_cls.MAX_PLAYERS,
            "estimated_time": game_cls.ESTIMATED_TIME,
            "category": game_cls.CATEGORY
        })
    return games_meta

def get_game_class(game_id: str) -> Type[BaseGame]:
    """Retrieves the game class for a given game_id."""
    return GAME_REGISTRY.get(game_id, FibbageGame)

__all__ = ["BaseGame", "GAME_REGISTRY", "list_games", "get_game_class"]
