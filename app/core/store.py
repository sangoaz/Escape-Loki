from app.schemas.game import ChatMessage


# Définition d'un objet python en mémoire afi de creer un système de stockage
class InMemoryGameStore:
    def __init__(self) -> None:
        self._players: dict[str, dict] = {}

    # Creation d'une nouvelle partie
    def create_player(
        self, player_id: str, initial_messages: list[ChatMessage]
    ) -> None:
        self._players[player_id] = {
            "current_phase": 1,
            "validated_keywords": [],
            "completed": False,
            "messages": initial_messages.copy(),
        }

    # Fonction servant à récuperer le joueur
    def get_player(self, player_id: str) -> dict | None:
        return self._players.get(player_id)

    # Mettre à jour un joueur
    def update_player(self, player_id: str, data: dict) -> None:
        self._players[player_id] = data


# Stockage mémoire simple pour la V1.
# Plus tard, ce composant pourra être remplacé par Redis, une DB SQL, etc.
game_store = InMemoryGameStore()
