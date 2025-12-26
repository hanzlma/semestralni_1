from collections import deque
import random
from typing import Literal

colors = {"z", "l", "c", "k"}
numbers = {"a", "7", "8", "9", "10", "k", "m", "s"}


class CardPack:
    """Parent Card pack class for visibility."""

    pass


class GiveCardPack(CardPack):
    """
    Card pack queue for giving cards.

    Attributes:
        cards (deque[str]): Card queue.
    """

    @staticmethod
    def generate_all_cards() -> list[str]:
        """
        Creates all card cominations from colors and numbers.

        Returns:
            list[str]: All cards.
        """
        return [f"{c}{n}" for c in colors for n in numbers]

    def __init__(self):
        """Initialize a GiveCardPack object with all cards in the pack."""
        self.cards = deque(GiveCardPack.generate_all_cards())
        random.shuffle(self.cards)

    def give_card(self) -> str | Literal[False]:
        """Gives a card from the card pack.

        Returns:
            (str | Literal[False]): The first card in queue. If the queue is empty, returns False.
        """
        if not len(self.cards):
            return False
        return self.cards.popleft()

    def add_cards(self, cards) -> None:
        """
        Adds cards to the end of the queue.

        Args:
            cards (list[str]): Cards to be added.
        """
        self.cards.extend(cards)


class PlayedCardPack(CardPack):
    """
    Played card pack class.

    Attributes:
        cards (deque[str]): Played cards.
    """

    def __init__(self):
        """Initialize the PlayedCardPack object with an empty pack."""
        self.cards = deque()

    def give_all_cards(self) -> deque[str]:
        """Empties itself apart from the last card and returns all other cards.

        Returns:
            deque[str]: Cards to be given.
        """
        cards = self.cards.copy()
        last_card = self.cards.pop()
        self.cards.clear()
        self.cards.append(last_card)
        return cards

    def add_card(self, card) -> None:
        """Adds a card to the pack.

        Args:
            card (str): Card to be added.
        """
        self.cards.append(card)

    def last_card(self) -> str:
        """Returns the last card from the pack.

        Returns:
            str: Last card.
        """
        return str(self.cards[-1])


class CardHand:
    """
    Class for players' card hands.

    Attributes:
        cards (list[str]): Cards in player's hand.
    """

    def __init__(self) -> None:
        """Initialize CardHand object with an empty hand."""
        self.cards = []

    def check_for_card(self, card: str) -> bool:
        """Checks if a card is in the hand.

        Args:
            card (str): Card to check.

        Returns:
            bool: True if card in hand else False.
        """
        return card in self.cards

    def play_card(self, card: str) -> bool:
        """Removes the card from hand if card in hand.

        Args:
            card (str): Card to be removed.

        Returns:
            bool: True if card in hand else False.
        """
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def add_card(self, card: str) -> None:
        """Adds a card to hand.

        Args:
            card (str): Card to be added.
        """
        self.cards.append(card)

    def list_cards(self) -> None:
        """Prints all cards in hand."""
        print(f"Available cards: {', '.join(self.cards)}")

    def get_card_count(self) -> int:
        """Returns the amount of cards in hand.

        Returns:
            int: Card count.
        """
        return len(self.cards)
