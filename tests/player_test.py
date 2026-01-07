import unittest as u
from player import ComputerPlayer, HumanPlayer


class PlayerTests(u.TestCase):
    def test_computer_player_list_cards_negative(self):
        self.assertNotIn("list_cards", dir(ComputerPlayer))

    def test_human_player_list_cards(self):
        self.assertIn("list_cards", dir(HumanPlayer))
