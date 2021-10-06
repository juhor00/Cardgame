class Status:

    def __init__(self, uid):
        """
        Create new status
        """
        self.uid = uid

        self.in_lobby = None
        self.lobby_ready = []
        self.opponents = []
        self.deck_amount = None
        self.gamedeck_amount = None
        self.claim_rank = None
        self.claim_amount = None
        self.display = []
        self.hand_cards = []
        self.play_cards = []
        self.allowed_claims = []
        self.denied_claims = []

    def set_lobby_status(self, status):
        self.in_lobby = status

    def is_in_lobby(self):
        return self.in_lobby
    
    def get_uid(self):
        return self.uid

    def add_opponent(self, uid, name):
        opponent = Opponent(uid, name)
        self.opponents.append(opponent)

    def get_opponent(self, uid):
        for opponent in self.opponents:
            if opponent.get_uid() == uid:
                return opponent

    def set_opponent_status(self, uid, status):
        """
        Set lobby ready status
        :param uid: int
        :param status: bool
        """
        opponent = self.get_opponent(uid)
        opponent.set_ready(status)

    def set_opponent_amount(self, uid, amount):
        opponent = self.get_opponent(uid)
        opponent.set_card_amount(amount)

    def set_deck_amount(self, amount):
        self.deck_amount = amount

    def get_deck_amount(self):
        return self.deck_amount

    def set_gamedeck_amount(self, amount):
        self.gamedeck_amount = amount

    def get_gamedeck_amount(self):
        return self.gamedeck_amount

    def set_claim(self, amount, rank):
        self.claim_rank = rank
        self.claim_amount = amount

    def set_display(self, cards):
        self.display = cards

    def get_display(self):
        return self.display

    def set_hand_cards(self, cards):
        self.hand_cards = cards

    def get_hand_cards(self):
        return self.hand_cards

    def set_allowed_claims(self, allowed):
        self.allowed_claims = allowed

    def get_allowed_claims(self):
        return self.allowed_claims

    def set_denied_claims(self, denied):
        self.denied_claims = denied

    def get_denied_claims(self):
        return self.denied_claims


class Opponent:

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        self.ready = None
        self.card_amount = 0

    def get_uid(self):
        return self.uid

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_ready(self, status):
        self.ready = status

    def is_ready(self):
        return self.ready

    def set_card_amount(self, amount):
        self.card_amount = amount

    def get_card_amount(self):
        return self.card_amount
