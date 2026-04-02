"""Contient la logique du jeu"""

import uuid
from dataclasses import dataclass

# Importation du contenu du scenario
from app.core.scenario import (
    PHASE_INTRO_MESSAGES,
    PHASE_CONFIG,
    PHASE_TRANSITION_MESSAGES,
    FINAL_UNLOCK_MESSAGES,
)
from app.core.store import game_store
from app.schemas.game import (
    ChatMessage,
    GameMessagesResponse,
    GameStartResponse,
    GameStateResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)


@dataclass
class ValidationResult:
    normalized_answer: str
    is_expected: bool
    already_found: bool
    phase_completed: bool
    game_completed: bool
    unlocked_messages: list[ChatMessage]
    feedback: str


class GameService:

    # Creation d'une partie propre et initialiser le début de jeu correctement
    def start_game(self) -> GameStartResponse:
        player_id = str(uuid.uuid4())

        # Récupération des messages d'introduction et convertion en objet ChatMessage
        initial_messages = [
            ChatMessage.model_validate(message) for message in PHASE_INTRO_MESSAGES
        ]

        # Enregistrement du joueur dans la mémoire du jeu
        game_store.create_player(player_id=player_id, initial_messages=initial_messages)

        return GameStartResponse(
            player_id=player_id,
            current_phase=1,
            completed=False,
            messages=initial_messages,
        )

    # Fonction récupérant l'état logique actuel de la partie
    def get_state(self, player_id: str) -> GameStateResponse | None:
        player = game_store.get_player(player_id)
        if player is None:
            return None

        return GameStateResponse(
            player_id=player_id,
            current_phase=player["current_phase"],
            validated_keywords=player["validated_keywords"],
            pending_keywords=self._get_pending_keywords(player),
            completed=player["completed"],
        )

    # Fonction récupérant le contenu conversationnel actuel de la partie
    def get_messages(self, player_id: str) -> GameMessagesResponse | None:
        player = game_store.get_player(player_id)
        if player is None:
            return None

        return GameMessagesResponse(
            player_id=player_id,
            current_phase=player["current_phase"],
            completed=player["completed"],
            messages=player["messages"],
        )

    # Réception de la réponse du joueur
    def submit_answer(
        self,
        payload: SubmitAnswerRequest,
    ) -> SubmitAnswerResponse | None:
        player = game_store.get_player(payload.player_id)
        if player is None:
            return None

        normalized_answer = self._normalize_keyword(payload.answer)

        if player["completed"]:
            player["messages"].append(
                ChatMessage(
                    sender="alex",
                    content=normalized_answer,
                    phase=player["current_phase"],
                    kind="answer",
                )
            )
            player["messages"].append(
                ChatMessage(
                    sender="system",
                    content="La partie est déjà terminée.",
                    phase=player["current_phase"],
                    kind="story",
                )
            )
            game_store.update_player(payload.player_id, player)

            return SubmitAnswerResponse(
                player_id=payload.player_id,
                is_correct=False,
                normalized_answer=normalized_answer,
                feedback="La partie est déjà terminée.",
                current_phase=player["current_phase"],
                validated_keywords=player["validated_keywords"],
                phase_completed=True,
                game_completed=True,
                unlocked_messages=[],
            )

        validation = self._validate_answer(player, payload.answer)

        player["messages"].append(
            ChatMessage(
                sender="alex",
                content=validation.normalized_answer,
                phase=player["current_phase"],
                kind="answer",
            )
        )

        if validation.is_expected and not validation.already_found:
            player["validated_keywords"].append(validation.normalized_answer)
            player["messages"].extend(validation.unlocked_messages)

            if validation.phase_completed and not validation.game_completed:
                player["current_phase"] += 1

            if validation.game_completed:
                player["completed"] = True
        else:
            player["messages"].append(
                ChatMessage(
                    sender=self._get_feedback_sender(player["current_phase"]),
                    content=validation.feedback,
                    phase=player["current_phase"],
                    kind="story",
                )
            )

        game_store.update_player(payload.player_id, player)

        return SubmitAnswerResponse(
            player_id=payload.player_id,
            is_correct=validation.is_expected and not validation.already_found,
            normalized_answer=validation.normalized_answer,
            feedback=validation.feedback,
            current_phase=player["current_phase"],
            validated_keywords=player["validated_keywords"],
            phase_completed=validation.phase_completed,
            game_completed=player["completed"],
            unlocked_messages=validation.unlocked_messages,
        )

    # Fonction de validation de la réponse
    def _validate_answer(self, player: dict, raw_answer: str) -> ValidationResult:
        current_phase = player["current_phase"]
        normalized_answer = self._normalize_keyword(raw_answer)
        phase_data = PHASE_CONFIG[current_phase]
        expected_keywords = phase_data["keywords"]

        # Vérifier que le mot n'a pas déjà été trouvé
        if normalized_answer in player["validated_keywords"]:
            return ValidationResult(
                normalized_answer=normalized_answer,
                is_expected=True,
                already_found=True,
                phase_completed=False,
                game_completed=False,
                unlocked_messages=[],
                feedback=self._build_feedback(current_phase, "already_found"),
            )

        # Vérifier que le mot soit juste
        if normalized_answer not in expected_keywords:
            return ValidationResult(
                normalized_answer=normalized_answer,
                is_expected=False,
                already_found=False,
                phase_completed=False,
                game_completed=False,
                unlocked_messages=[],
                feedback=self._build_feedback(current_phase, "wrong"),
            )

        # Setup du prochain mot à trouver
        phase_validated = [
            word for word in player["validated_keywords"] if word in expected_keywords
        ]
        next_expected_keyword = expected_keywords[len(phase_validated)]

        # Si le mot tapé n'est pas le prochain mot à trouver mais qu'il est quand même dans la liste des mots à trouver
        if normalized_answer != next_expected_keyword:
            return ValidationResult(
                normalized_answer=normalized_answer,
                is_expected=False,
                already_found=False,
                phase_completed=False,
                game_completed=False,
                unlocked_messages=[],
                feedback=self._build_feedback(current_phase, "wrong_order"),
            )

        unlocked_messages = self._messages_for_keyword(
            current_phase=current_phase,
            keyword=normalized_answer,
        )

        future_validated = [*player["validated_keywords"], normalized_answer]
        phase_completed = all(word in future_validated for word in expected_keywords)
        game_completed = current_phase == 3 and phase_completed

        if phase_completed:
            if current_phase in PHASE_TRANSITION_MESSAGES:
                unlocked_messages.extend(
                    [
                        ChatMessage.model_validate(message)
                        for message in PHASE_TRANSITION_MESSAGES[current_phase]
                    ]
                )
            if game_completed:
                unlocked_messages.extend(
                    [
                        ChatMessage.model_validate(message)
                        for message in FINAL_UNLOCK_MESSAGES
                    ]
                )

        return ValidationResult(
            normalized_answer=normalized_answer,
            is_expected=True,
            already_found=False,
            phase_completed=phase_completed,
            game_completed=game_completed,
            unlocked_messages=unlocked_messages,
            feedback="Bonne réponse.",
        )

    # Récupération des messages associés à un mot précis dans une phase précise
    def _messages_for_keyword(
        self, current_phase: int, keyword: str
    ) -> list[ChatMessage]:
        raw_messages = PHASE_CONFIG[current_phase]["keyword_messages"].get(keyword, [])
        return [ChatMessage.model_validate(message) for message in raw_messages]

    # Fonction qui permet d'éviter la casse
    def _normalize_keyword(self, value: str) -> str:
        return " ".join(value.strip().upper().split())

    # Calcule les mots restants à trouver dans l'étape en cours
    def _get_pending_keywords(self, player: dict) -> list[str]:
        current_phase = player["current_phase"]
        expected = PHASE_CONFIG[current_phase]["keywords"]
        return [
            keyword
            for keyword in expected
            if keyword not in player["validated_keywords"]
        ]

    def _build_feedback(self, current_phase: int, feedback_type: str) -> str:
        feedbacks = {
            1: {
                "wrong": "Non… ce n’est pas ça. Nous avons du passer à côté de quelque chose.",
                "already_found": "Tu l’as déjà trouvé. Je ne pense pas que cela vaille la peine que l'on revienne dessus...",
                "wrong_order": "Pas encore… Il y a un autre élément à découvrir avant celui-ci.",
            },
            2: {
                "wrong": "AHAHAHA… Non. Tu ne trouveras jamais mon trésor.",
                "already_found": "Tu radotes. Ce mot a déjà été validé.",
                "wrong_order": "Allons, allons… Tu brûles les étapes. Trouve d’abord ce qui vient avant.",
            },
            3: {
                "wrong": "AHAHAHAHAHA, tu ne trouveras jamais la source de mon pouvoir.",
                "already_found": "Tu t’acharnes pour rien. Ce mot a déjà servi.",
                "wrong_order": "Tu n’y es pas encore… il te manque encore une compréhension essentielle.",
            },
        }

        return feedbacks[current_phase][feedback_type]

    # Si la réponse est fausse, milo répond dans la phase 1 et loki dans les deux secondes phases
    def _get_feedback_sender(self, current_phase: int) -> str:
        if current_phase == 1:
            return "milo"
        return "loki"


game_service = GameService()
