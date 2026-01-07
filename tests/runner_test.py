import unittest as u
from cards import GiveCardPack, PlayedCardPack
from game_runner import GameRunner
from player import ComputerPlayer, HumanPlayer
from unittest.mock import patch


class RunnerTests(u.TestCase):
    def setUp(self):
        self.runner = GameRunner()

    def test_init(self):
        self.assertIsInstance(self.runner.computer_player, ComputerPlayer)
        self.assertIsInstance(self.runner.human_player, HumanPlayer)
        self.assertIsInstance(self.runner.give_card_pack, GiveCardPack)
        self.assertIsInstance(self.runner.played_card_pack, PlayedCardPack)
        self.assertFalse(
            self.runner.played, "Attribute played should be False after init."
        )
        self.assertFalse(
            self.runner.active_card, "Attribute active_card should be False after init."
        )
        self.assertIsNone(
            self.runner.desired_color,
            "Attribute desired_color should be None after init.",
        )
        self.assertEqual(
            self.runner.stacking, 0, "Attribute stacking should be 0 after init."
        )
        self.assertEqual(
            len(self.runner.human_player.card_hand.cards),
            4,
            "Human player should have 4 cards after init.",
        )
        self.assertEqual(
            len(self.runner.computer_player.card_hand.cards),
            4,
            "Computer player should have 4 cards after init.",
        )
        self.assertEqual(
            len(self.runner.give_card_pack.cards),
            23,
            "Give card pack should hold 23 cards after init.",
        )
        self.assertEqual(
            len(self.runner.played_card_pack.cards),
            1,
            "There should be a single card in played card pack after init.",
        )

    def test_check_card_playable_positive(self):
        self.runner.played_card_pack.add_card("l8")
        self.assertTrue(
            self.runner.check_card_playable("z8"),
            "Method check_card_playable should return True for last played l8 and card z8.",
        )

    def test_check_card_playable_negative(self):
        self.runner.played_card_pack.add_card("l8")
        self.assertFalse(
            self.runner.check_card_playable("z9"),
            "Method check_card_playable should return False for last played l8 and card z9.",
        )

    def test_playable_sim_positive(self):
        self.assertTrue(
            self.runner._is_playable_sim("z8", "l8"),
            "Method _is_playable_sim should return True for last played l8 and card z8.",
        )

    def test_playable_sim_negative(self):
        self.assertFalse(
            self.runner._is_playable_sim("z9", "l8"),
            "Method _is_playable_sim should return False for last played l8 and card z9.",
        )

    def test_get_valid_moves_default(self):
        self.assertEqual(
            self.runner._get_valid_moves(["l7", "ka", "kk"], "lk", False),
            [("l7", None), ("kk", None)],
            "Method _get_valid_moves should return both l7 and kk as they are both playable after lk.",
        )

    def test_get_valid_moves_inactive_seven(self):
        self.assertEqual(
            self.runner._get_valid_moves(["lk", "ka", "k7"], "l7", False),
            [("lk", None), ("k7", None)],
            "Method _get_valid_moves should return both lk and k7 as they are both playable after l7 when it is not active.",
        )

    def test_get_valid_moves_inactive_ace(self):
        self.assertEqual(
            self.runner._get_valid_moves(["lk", "k7", "ka"], "la", False),
            [("lk", None), ("ka", None)],
            "Method _get_valid_moves should return both lk and ka as they are both playable after la when it is not active.",
        )

    def test_get_valid_moves_active_seven(self):
        self.assertEqual(
            self.runner._get_valid_moves(["lk", "ka", "k7"], "l7", True),
            [("k7", None)],
            "Method _get_valid_moves should return only k7 since it is the only card playable after l7 when it is active.",
        )

    def test_get_valid_moves_active_ace(self):
        self.assertEqual(
            self.runner._get_valid_moves(["lk", "k7", "ka"], "la", True),
            [("ka", None)],
            "Method _get_valid_moves should return only ka since it is the only card playable after la when it is active.",
        )

    def test_get_valid_moves_color_change(self):
        self.assertEqual(
            self.runner._get_valid_moves(
                ["l7", "z7", "c7"], "lm", True
            ),  # get_valid_moves gets the color changer with the selected color already
            [("l7", None)],
            "Method _get_valid_moves should return only l7.",
        )

    def test_get_valid_moves_empty_invalid_color_and_type(self):
        self.assertEqual(
            self.runner._get_valid_moves(["c7", "ca"], "lk", False),
            [],
            "Method _get_valid_moves should return an empty array when there are no cards to be played of the matching color and type.",
        )

    def test_get_valid_moves_empty_after_ace(self):
        self.assertEqual(
            self.runner._get_valid_moves(["c7", "ck"], "ca", True),
            [],
            "Method _get_valid_moves should return an empty array when there are no cards to be played because of an active ace card.",
        )

    def test_get_valid_moves_empty_after_seven(self):
        self.assertEqual(
            self.runner._get_valid_moves(["ca", "ck"], "c7", True),
            [],
            "Method _get_valid_moves should return an empty array when there are no cards to be played because of an active 7 card.",
        )

    def test_minimax_win(self):
        self.assertEqual(
            self.runner.minimax(["lk"], ["z8"], "l9", False, 2, True),
            (100, ("lk", None)),
            "Minimax should return the only card the computer has, and score 100, because he will win.",
        )

    def test_minimax_lose(self):
        self.assertEqual(
            self.runner.minimax(["lk"], ["z9"], "l9", False, 2, False),
            (-100, ("z9", None)),
            "Minimax should return the only card the player has, and score -100, because he will win.",
        )

    def test_minimax_win_two_turns(self):
        self.assertEqual(
            self.runner.minimax(["lk", "kk"], ["z8"], "l9", False, 4, True),
            (10, ("lk", None)),
            "Minimax should return the only playable card, and score 10, because he will not win yet.",
        )

    def test_minimax_correct_card_order(self):
        self.assertEqual(
            self.runner.minimax(["l8", "lk"], ["z8"], "l9", False, 4, True),
            (10, ("lk", None)),
            "Minimax should return the card lk, because l8 would let the human play, and score 10, because he will not win yet.",
        )

    def test_minimax_take_card(self):
        self.assertEqual(
            self.runner.minimax(["kk"], ["z8"], "l9", False, 4, True),
            (-10, None),
            "Minimax should return score -10 because he cannot play any cards.",
        )

    def test_play_card(self):
        self.runner.human_player.card_hand.cards = ["lk"]
        self.runner.played_card_pack.cards = ["kk"]
        self.assertTrue(
            self.runner.play_card(self.runner.human_player, "lk"),
            "Should return True since it is a valid move.",
        )
        self.assertEqual(
            self.runner.human_player.card_hand.cards,
            [],
            "The played card should be removed from the player's hand.",
        )
        self.assertEqual(
            self.runner.played_card_pack.cards,
            ["kk", "lk"],
            "The played card should be added to the played card pack.",
        )

    @patch("builtins.print")
    def test_play_card_not_in_pack(self, mock_print):
        self.runner.human_player.card_hand.cards = ["zk"]
        self.runner.played_card_pack.cards = ["kk"]
        self.assertFalse(
            self.runner.play_card(self.runner.human_player, "lk"),
            "Should return False since it is not a valid move. Player doesn't have that card.",
        )
        self.assertNotIn(
            "zk",
            self.runner.played_card_pack.cards,
            "Since player could not play that card, it should not be added to the played card pack.",
        )
        self.assertEqual(
            self.runner.human_player.card_hand.cards,
            ["zk"],
            "Player's hand should not change after an invalid play.",
        )
        mock_print.assert_called_with(
            "You dont have the card you want to play. Play a different card or take a card."
        )

    @patch("builtins.print")
    def test_play_card_negative(self, mock_print):
        self.runner.human_player.card_hand.cards = ["zk"]
        self.runner.played_card_pack.cards = ["l9"]
        self.assertFalse(
            self.runner.play_card(self.runner.human_player, "zk"),
            "Should return False since it is not a valid move.",
        )
        self.assertNotIn(
            "zk",
            self.runner.played_card_pack.cards,
            "Since player could not play that card, it should not be added to the played card pack.",
        )
        mock_print.assert_called_with("You cannot play this card now.")

    @patch("builtins.input", return_value="Easy")
    def test_select_difficulty_easy(self, mock_input):
        self.runner.select_difficulty()
        self.assertTrue(
            self.runner.easy,
            "After setting difficulty to easy, the attribute should be True.",
        )

    @patch("builtins.input", return_value="Hard")
    def test_select_difficulty_hard(self, mock_input):
        self.runner.select_difficulty()
        self.assertFalse(
            self.runner.easy,
            "After setting difficulty to hard, the attribute should be False.",
        )
