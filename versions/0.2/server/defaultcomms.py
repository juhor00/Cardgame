"""
Default comminuication data
For initalizing clients and such
"""


join_info = {}


game_init_info = {
                "player": {"add": ["2S", "10D", "QS", "3S", "8H", "JS", "10H", "2S", "10D", "QS", "3S", "8H", "JS", "10H"]},
                "opponent": [
                        {"Juuso": {"amount": 10,
                                   "won": 0,
                                   "lost": 0}
                         },
                        {"Petteri": {"amount": 3,
                                     "won": 0,
                                     "lost": 0}
                         }
                        ],
                "deck": {"amount": 10,
                         "drawtop": "2D"},
                "game": {"latest": {"amount": 3,
                                    "rank": "J"},
                         "amount": 2,
                         "suspect": {"cards": ["8D, 9H"],
                                     "lied": 1}
                         },
                "sidebar": {"allowed": ["J", "Q", "K", "A", "2"],
                            "denied": ["3", "4", "5"]}

            }
