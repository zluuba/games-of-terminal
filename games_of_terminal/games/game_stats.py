from dataclasses import dataclass


@dataclass
class GameStats:
    game_status: str = 'game_active'

    score: int = 0
    best_score: int = 0

    is_pause: bool = False
    is_exit: bool = False
    is_restart: bool = False
