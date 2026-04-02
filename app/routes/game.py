from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.schemas.game import (
    GameMessagesResponse,
    GameStartResponse,
    GameStartRequest,
    GameStateResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.services.game_service import game_service

router = APIRouter(prefix="/game", tags=["game"])

# Emplacement de mon template
templates = Jinja2Templates(directory="app/templates")


# Route de création de partie / joueur / session
@router.post(
    "/start",
    response_model=GameStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_game(payload: GameStartRequest) -> GameStartResponse:
    return game_service.start_game(payload)


# Afficher la page de départ
@router.get("/start-page", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("start.html", {"request": request})


# Affiche le front (le chat)
@router.get("/play", response_class=HTMLResponse)
def play(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Récupère l'etat du joueur (étape actuelle, énigme en cours, progression)
@router.get("/state/{player_id}", response_model=GameStateResponse)
def get_game_state(player_id: str) -> GameStateResponse:
    state = game_service.get_state(player_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return state


# Récupère les messages du chat
@router.get("/messages/{player_id}", response_model=GameMessagesResponse)
def get_game_messages(player_id: str) -> GameMessagesResponse:
    messages = game_service.get_messages(player_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return messages


# Coeur du gameplay, elle soumet la réponse utilisateur
@router.post("/submit", response_model=SubmitAnswerResponse)
def submit_answer(payload: SubmitAnswerRequest) -> SubmitAnswerResponse:
    result = game_service.submit_answer(payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return result
