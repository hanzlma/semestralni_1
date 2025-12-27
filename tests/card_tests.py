import unittest as u
from collections import deque
from cards import GiveCardPack, PlayedCardPack, CardHand


class Cards(u.TestCase):
    def test_givecard_instance(self):
        self.assertIsInstance(
            GiveCardPack().cards,
            deque,
            f"GiveCardPack cards should be of instance deque[str] not {type(GiveCardPack().cards)}",
        )

    def test_playedcard_instance(self):
        self.assertIsInstance(
            PlayedCardPack().cards,
            deque,
            f"GiveCardPack cards should be of instance deque[str] not {type(PlayedCardPack().cards)}",
        )

    def test_cardhand_instance(self):
        self.assertIsInstance(
            CardHand().cards,
            list,
            f"CardHand should be of instance list not {type(CardHand().cards)}",
        )

    def test_generate_cards(self):
        expected_cards = [
            "la",
            "l7",
            "l8",
            "l9",
            "l10",
            "lk",
            "lm",
            "ls",
            "ka",
            "k7",
            "k8",
            "k9",
            "k10",
            "kk",
            "km",
            "ks",
            "ca",
            "c7",
            "c8",
            "c9",
            "c10",
            "ck",
            "cm",
            "cs",
            "za",
            "z7",
            "z8",
            "z9",
            "z10",
            "zk",
            "zm",
            "zs",
        ]
        generated_cards = GiveCardPack.generate_all_cards()
        difference_genereted = [
            card for card in generated_cards if card not in expected_cards
        ]
        difference_expected = [
            card for card in expected_cards if card not in generated_cards
        ]
        self.assertEqual(
            len(difference_genereted),
            0,
            f'These cards: "{", ".join(difference_genereted)}" should not have been generated.',
        )
        self.assertEqual(
            len(difference_expected),
            0,
            f'These cards: "{", ".join(difference_expected)}" should have been generated but weren\'t.',
        )

    def test_give_card(self):
        pack = GiveCardPack()
        given_card = pack.give_card()
        self.assertIn(
            given_card,
            GiveCardPack.generate_all_cards(),
            f'Give card returned a card ("{given_card}") which should not be in a give_card pack.',
        )

    def test_give_card_empty(self):
        pack = GiveCardPack()
        for _ in range(32):
            pack.give_card()
        given = pack.give_card()
        self.assertFalse(
            given, f'Give card should have returned false, returned "{given}" instead.'
        )

    def test_give_all_cards(self):
        pack = PlayedCardPack()
        pack.cards = GiveCardPack.generate_all_cards()
        last = pack.last_card()
        pack.give_all_cards()
        self.assertEqual(
            len(pack.cards),
            1,
            f"Exactly one card should remain in the pack, instead {len(pack.cards)} remained",
        )
        self.assertIn(
            last,
            pack.cards,
            f'"{last}" should have remained in the pack, instead "{pack.cards[-1]}" remained',
        )
