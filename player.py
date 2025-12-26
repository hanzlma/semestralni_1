from cards import CardHand


class Player:
    """
    Player class.

    Attributes:
        card_hand (CardHand): Card hand of the player.
    """

    def __init__(self):
        """Initialize the Player object."""
        self.card_hand = CardHand()

    def check_for_card(self, card: str) -> bool:
        """Checks if a card is in player's hand.

        Args:
            card (str): Card to be checked.

        Returns:
            bool: True if card in hand else False.
        """
        return self.card_hand.check_for_card(card)

    def play_card(self, card: str) -> bool:
        """Removes a card from player's hand.

        Args:
            card (str): Card to be removed.

        Returns:
            bool: True if card in hand else False.
        """
        return self.card_hand.play_card(card)

    def add_card(self, card: str) -> None:
        """Adds a card to player's hand.

        Args:
            card (str): Card to be added.
        """
        self.card_hand.add_card(card)

    def get_card_count(self) -> int:
        """Returns the amount of cards in player's hand.

        Returns:
            int: Card count.
        """
        return self.card_hand.get_card_count()


class HumanPlayer(Player):
    """Human player class for visibility purposes."""

    def __init__(self):
        """Initialize the HumanPlayer object."""
        super().__init__()

    def list_cards(self) -> None:
        """Show human player's available cards."""
        self.card_hand.list_cards()


class ComputerPlayer(Player):
    """Computer player class for visibility purposes."""

    def __init__(self):
        """Initialize the ComputerPlayer object."""
        super().__init__()
