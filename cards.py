from collections import deque
import random

colors = {"z", "l", "c", "k"}
numbers = {"a", "7", "8", "9", "10", "k", "m", "s"}


class CardPack:
    pass


class GiveCardPack(CardPack):
    @staticmethod
    def generate_all_cards():
        return [f"{c}{n}" for c in colors for n in numbers]

    def __init__(self):
        self.cards = deque(GiveCardPack.generate_all_cards())
        random.shuffle(self.cards)

    def give_card(self):
        if not len(self.cards):
            return False
        return self.cards.popleft()

    def add_cards(self, cards):
        self.cards.extend(cards)


class PlayedCardPack(CardPack):
    def __init__(self):
        self.cards = deque()

    def give_all_cards(self):
        cards = self.cards.copy()
        last_card = self.cards.pop()
        self.cards.clear()
        self.cards.append(last_card)
        return cards

    def add_card(self, card):
        self.cards.append(card)

    last_card = lambda self: str(self.cards[len(self.cards) - 1])  # noqa: E731


class CardHand:
    def __init__(self):
        self.cards = []

    def check_for_card(self, card) -> bool:
        return card in self.cards

    def play_card(self, card) -> bool:
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def add_card(self, card):
        self.cards.append(card)

    def list_cards(self):
        print(f"Available cards: {', '.join(self.cards)}")

    def get_card_count(self):
        return len(self.cards)
