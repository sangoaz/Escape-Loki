PHASE_INTRO_MESSAGES = [
    {
        "sender": "milo",
        "content": (
            "Maman… Je sais que ça paraît bizarre… mais là, c’est vraiment "
            "important. C’est à propos de Loki."
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Il faisait partie de l’équipe de Lapin qui devait livrer les chocolats "
            "de Pâques… puis il a goûté les Kinder. Tous."
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Et depuis… Il n’est plus le même... "
            "Ces chocolats, ce ne sont pas de simples chocolats"
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Ils contiennent un pouvoir sombre..."
            "Que personne ne devrait absorber seul, mais Loki, il les a tous pris"
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Depuis, il n’est plus le même. Il les a cachés. Tu es la seule qui "
            "peut les retrouver sans être corrompue."
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Laisse-moi t’aider… et ensemble, on va le ramener à la raison,"
            "et retrouver les chocolats qu’il a cachés."
        ),
        "phase": 1,
        "kind": "story",
    },
    {
        "sender": "milo",
        "content": (
            "Pour commencer, je crois que Loki a caché le premier chocolat dans ton carburant matinal"
        ),
        "phase": 1,
        "kind": "hint",
    },
]

PHASE_CONFIG = {
    1: {
        "keywords": ["CAFE", "LIVRE", "CAROTTE", "CHEMINEE", "ASPIRATEUR", "PAILLE"],
        "keyword_messages": {
            "CAFE": [
                {
                    "sender": "milo",
                    "content": (
                        "Bien vu… Pour le second: "
                        "Sans connaître le néon, ni le studio… Loki a tenté de s’échapper aux alentours de Brisbane."
                    ),
                    "phase": 1,
                    "kind": "hint",
                }
            ],
            "LIVRE": [
                {
                    "sender": "milo",
                    "content": (
                        "Déjà deux ! Pour celui là tu demandes toujours la permission à Papa si tu peux lui en donner"
                    ),
                    "phase": 1,
                    "kind": "hint",
                }
            ],
            "CAROTTE": [
                {
                    "sender": "milo",
                    "content": (
                        "Je crois que nous sommes à la moitié! "
                        "Attention pour celui là… Loki, lui, ne l’a pas confondu avec sa litière… il sait qu’il pourrait se bruler les fesses"
                    ),
                    "phase": 1,
                    "kind": "hint",
                }
            ],
            "CHEMINEE": [
                {
                    "sender": "milo",
                    "content": (
                        "Oui… un endroit chaleureux... "
                        "Maintenant, l'endroit où se trouve le prochain est un endroit qui engloutit tout sur son passage, même les 'secrets' de Loki n'y échappent pas"
                    ),
                    "phase": 1,
                    "kind": "hint",
                }
            ],
            "ASPIRATEUR": [
                {
                    "sender": "milo",
                    "content": (
                        "Aaaaah, il déteste ce monstre bruyant! "
                        "Pour le dernier, il se trouve dans son stock de carburant"
                    ),
                    "phase": 1,
                    "kind": "hint",
                }
            ],
            "PAILLE": [
                {
                    "sender": "milo",
                    "content": "Bravo ! C'était son dernier chocolat... Attends... Il arrive !",
                    "phase": 1,
                    "kind": "story",
                }
            ],
        },
    },
    2: {
        "keywords": ["CAGE", "MAXI"],
        "keyword_messages": {
            "CAGE": [
                {
                    "sender": "milo",
                    "content": "La cage… évidemment. C’est là qu’il a laissé son ancienne vie derrière lui.",
                    "phase": 2,
                    "kind": "hint",
                },
                {
                    "sender": "loki",
                    "content": "Nooooooooooooooooooooooooooooooooon !! 😆 Sérieusement !? ",
                    "phase": 2,
                    "kind": "story",
                },
            ],
            "MAXI": [
                {
                    "sender": "loki",
                    "content": "Tu pensais avoir récupéré tout mon trésor ? Il ne s’agit que d’une infime partie AHAHAHAHAHAH",
                    "phase": 2,
                    "kind": "story",
                }
            ],
        },
    },
    3: {
        "keywords": ["GARAGE"],
        "keyword_messages": {
            "GARAGE": [
                {
                    "sender": "milo",
                    "content": (
                        "Les indices pour trouver son trésor sont cachés dans ses émotions… "
                        "et toi, tu viens de les comprendre."
                    ),
                    "phase": 3,
                    "kind": "story",
                },
                {
                    "sender": "loki",
                    "content": "Non… Attends. Ne va surtout pas par là... Tu ne comprends pas ce que tu fais.",
                    "phase": 3,
                    "kind": "story",
                },
            ]
        },
    },
}

PHASE_TRANSITION_MESSAGES = {
    1: [
        {
            "sender": "loki",
            "content": (
                "Oh… Bravo Maman 😅"
                "Impressionnant ! Je ne pensais pas que tu irais aussi loin. "
                "Milo t’aide, n’est-ce pas ? 😀 "
                "Toujours aussi fidèle… Pathétique. 😍 "
                "Tu crois vraiment pouvoir me stopper ? 😀 Très bien. "
                "Voyons jusqu’où tu es prête à aller. 😅"
            ),
            "phase": 2,
            "kind": "story",
        },
        {
            "sender": "milo",
            "content": (
                "Tu vois ce que je te disais… Il est devenu complètement fou… "
                "Les chocolats l’ont totalement corrompu. "
                "Mais attends… Tout ce qu’on a trouvé jusqu’ici… "
                "Ce n’est pas pour rien. Regarde bien les éléments… Ils doivent former quelque chose."
            ),
            "phase": 2,
            "kind": "story",
        },
    ],
    2: [
        {
            "sender": "milo",
            "content": "Il semblerait que Loki ait encore une part de conscience…",
            "phase": 3,
            "kind": "story",
        },
        {
            "sender": "milo",
            "content": (
                "Les indices pour trouver son trésor sont cachés dans ses émotions. "
                "Et j’ai l’impression que… Certaines d’entre elles ont déjà parlé."
            ),
            "phase": 3,
            "kind": "hint",
        },
    ],
}

FINAL_UNLOCK_MESSAGES = [
    {
        "sender": "milo",
        "content": "Bravo. Le passage vers le trésor final est maintenant ouvert.",
        "phase": 3,
        "kind": "story",
    },
    {
        "sender": "system",
        "content": "Un message final apparaît sur le billard…",
        "phase": 3,
        "kind": "story",
    },
]
