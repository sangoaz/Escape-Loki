from typing import Literal

from pydantic import BaseModel, Field


SenderType = Literal["milo", "loki", "alex", "system"]
MessageKind = Literal["story", "hint", "answer"]


# Message du chat
class ChatMessage(BaseModel):
    sender: SenderType
    content: str
    phase: int = Field(ge=1, le=3)
    kind: MessageKind = "story"


# La réponse lorsque l'on commence une partie
class GameStartResponse(BaseModel):
    player_id: str
    current_phase: int
    completed: bool
    messages: list[ChatMessage]


# L'état logique actuel du jeu
class GameStateResponse(BaseModel):
    player_id: str
    current_phase: int
    validated_keywords: list[str]
    pending_keywords: list[str]
    completed: bool


# Ce que le joueur renvoie
class SubmitAnswerRequest(BaseModel):
    player_id: str
    answer: str = Field(min_length=1, max_length=100)


# Ce que le backend répond après une tentative de réponse
class SubmitAnswerResponse(BaseModel):
    player_id: str
    is_correct: bool
    normalized_answer: str
    feedback: str
    current_phase: int
    validated_keywords: list[str]
    phase_completed: bool
    game_completed: bool
    unlocked_messages: list[ChatMessage]


# Historique du chat
class GameMessagesResponse(BaseModel):
    player_id: str
    current_phase: int
    completed: bool
    messages: list[ChatMessage]
