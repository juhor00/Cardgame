from copy import copy


def compare(a, b):
    """
    Return a if a!=b, else None
    :param a:
    :param b:
    :return: type(a) or None
    """
    if a != b:
        return a
    else:
        return None


def list_difference(a, b):
    """
    Return difference of lists as sets.
    First set has elements that are in a but not in b.
    Second set has elements that are in b but not in a.
    Duplicates in lists are ignored as they convert to set.
    :param a: list
    :param b: list
    :return: tuple of sets
    """
    a = set(a)
    b = set(b)
    return a-b, b-a


class Status:

    def __init__(self, uid):
        """
        Create new status
        """
        self.uid = uid

        self.in_lobby = None
        self.opponents = []
        self.deck_amount = None
        self.gamedeck_amount = None
        self.claim = None
        self.display = []
        self.hand_cards = []
        self.play_cards = []
        self.allowed_claims = []
        self.denied_claims = []
        self.turn = None
        self.duration = None

    def __str__(self):
        return str(vars(self))

    def compare(self, other: 'Status'):
        """
        Compares two Status instances and returns the difference as Changes
        Result values are defined by this instance
        :param other: Status
        :return: Changes or None, None if uid does not match
        """
        if self.get_uid() != other.get_uid():
            return None

        change = Changes()
        self_vars = vars(self)
        other_vars = vars(other)

        for self_attr, other_attr in zip(self_vars, other_vars):
            if self_attr == 'uid':
                continue
            self_val = self_vars[self_attr]
            other_val = other_vars[other_attr]

            # Lists
            if type(self_val) is list:
                # Claim buttons
                if self_attr in ["allowed_claims", "denied_claims"]:
                    res_val = compare(self_val, other_val)
                    change.add_attribute(self_attr, res_val)

                # Opponents
                elif self_attr == "opponents":
                    modify, add, remove = self.compare_opponents(other_val)
                    change.add_attribute(self_attr+'_modify', modify)
                    change.add_attribute(self_attr+'_add', add)
                    change.add_attribute(self_attr + '_remove', remove)

                # Card lists
                else:
                    add, remove = list_difference(self_val, other_val)
                    change.add_attribute(self_attr+'_add', add)
                    change.add_attribute(self_attr+'_remove', remove)

            # Other attributes
            else:
                res_val = compare(self_val, other_val)
                change.add_attribute(self_attr, res_val)

        return change

    def compare_opponents(self, opponents):
        """
        Compares opponents and return list of opponents with changes
        :param opponents: list of opponents
        :return: list of opponents
        """
        modify = []
        remove = []
        add = []

        for other_opponent in opponents:

            uid = other_opponent.get_uid()
            self_opponent = self.get_opponent(uid)

            # Remove
            if self_opponent is None:
                remove.append(copy(other_opponent))
                continue

            # Modify
            if not (self_opponent == other_opponent):
                modify.append(copy(self_opponent))

        # Add
        for self_opponent in self.opponents:
            uid = self_opponent.get_uid()
            add.append(copy(self_opponent))
            for other_opponent in opponents:
                # Uid found in other opponents
                if other_opponent.get_uid() == uid:
                    add.remove(self_opponent)
                    break

        return modify, add, remove

    def set_lobby_status(self, status):
        self.in_lobby = status

    def is_in_lobby(self):
        return self.in_lobby
    
    def get_uid(self):
        return self.uid

    def add_opponent(self, uid, name):
        opponent = self.get_opponent(uid)
        if opponent is None:
            opponent = Opponent(uid, name)
            self.opponents.append(opponent)
            return
        else:
            opponent.set_name(name)

    def get_opponent(self, uid):
        for opponent in self.opponents:
            if opponent.get_uid() == uid:
                return opponent
        return None

    def get_all_opponent_uids(self):
        uids = []
        for opponent in self.opponents:
            uids.append(opponent.get_uid())
        return uids

    def get_opponents(self):
        return self.opponents

    def remove_opponent(self, uid):
        opponent = self.get_opponent(uid)
        self.opponents.remove(opponent)

    def set_opponent_name(self, uid, name):
        opponent = self.get_opponent(uid)
        opponent.set_name(name)

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

    def set_opponent_turn(self, uid, turn):
        opponent = self.get_opponent(uid)
        opponent.set_turn(turn)

    def set_opponent_played(self, uid, played):
        opponent = self.get_opponent(uid)
        opponent.set_played(played)

    def set_opponent_suspected(self, uid, suspected):
        opponent = self.get_opponent(uid)
        opponent.set_suspected(suspected)

    def set_deck_amount(self, amount):
        self.deck_amount = amount

    def get_deck_amount(self):
        return self.deck_amount

    def set_gamedeck_amount(self, amount):
        self.gamedeck_amount = amount

    def get_gamedeck_amount(self):
        return self.gamedeck_amount

    def set_claim(self, amount, rank):
        self.claim = (amount, rank)

    def set_display(self, cards):
        self.display = cards

    def get_display(self):
        return self.display

    def is_displaying(self):
        return len(self.get_display()) > 0

    def set_hand_cards(self, cards):
        """
        Set hand cards. If card is already in play cards, and player is in turn, don't change
        :param cards: list of str
        """
        corrected_cards = []
        for card in cards:
            if card in self.play_cards:
                if self.is_in_turn():
                    continue
                else:
                    corrected_cards.append(card)
                    self.play_cards.remove(card)
            else:
                corrected_cards.append(card)

        self.hand_cards = corrected_cards

    def get_hand_cards(self):
        return self.hand_cards

    def set_play_cards(self, cards):
        self.play_cards = cards

    def get_play_cards(self):
        return self.play_cards

    def set_allowed_claims(self, allowed):
        self.allowed_claims = allowed

    def get_allowed_claims(self):
        return self.allowed_claims

    def set_denied_claims(self, denied):
        self.denied_claims = denied

    def get_denied_claims(self):
        return self.denied_claims

    def set_turn(self, turn):
        self.turn = turn

    def is_in_turn(self):
        return self.turn

    def set_duration(self, duration):
        self.duration = duration


class Changes:

    def __init__(self):
        pass

    def __str__(self):
        return str(vars(self))

    def add_attribute(self, name, value):

        if value is None:
            return

        if type(value) is set:
            value = list(value)

        if type(value) is list:
            if not value:
                return

        self.__setattr__(name, value)

    def get_attributes(self):
        return vars(self)


class Opponent:

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        self.ready = None
        self.card_amount = 0
        self.turn = None
        self.played = None
        self.suspected = None

    def __eq__(self, other: 'Opponent'):
        if self.get_uid() != other.get_uid():
            return False
        if self.get_name() != other.get_name():
            return False
        if self.is_ready() != other.is_ready():
            return False
        if self.get_card_amount() != other.get_card_amount():
            return False
        if self.is_in_turn() != other.is_in_turn():
            return False
        if self.has_played() != other.has_played():
            return False
        if self.has_suspected() != other.has_suspected():
            return False
        return True

    def __str__(self):
        return f"{self.get_uid()} {self.get_name()}"

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

    def set_turn(self, turn):
        self.turn = turn

    def is_in_turn(self):
        return self.turn

    def set_played(self, played: bool):
        self.played = played

    def has_played(self):
        return self.played

    def set_suspected(self, suspected: bool):
        self.suspected = suspected

    def has_suspected(self):
        return self.suspected