from cards import CardHand


class Player:
    def __init__(self):
        self.card_hand = CardHand()

    def check_for_card(self, card):
        return self.card_hand.check_for_card(card)

    def play_card(self, card):
        return self.card_hand.play_card(card)

    def add_card(self, card):
        self.card_hand.add_card(card)

    def get_card_count(self):
        return self.card_hand.get_card_count()


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def list_cards(self):
        self.card_hand.list_cards()


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
