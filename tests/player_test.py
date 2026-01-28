import unittest as u
from player import ComputerPlayer, HumanPlayer


class PlayerTests(u.TestCase):
    """Tests involving Player class and its descendants."""

    def test_computer_player_list_cards_negative(self):
        """Computer player does not have method list_cards test."""
        self.assertNotIn("list_cards", dir(ComputerPlayer))

    def test_human_player_list_cards(self):
        """Human player has list cards method test."""
        self.assertIn("list_cards", dir(HumanPlayer))
