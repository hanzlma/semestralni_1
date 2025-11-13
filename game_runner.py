import operator
from player import Player, HumanPlayer, ComputerPlayer
from cards import GiveCardPack, PlayedCardPack


class GameRunner:
    def __init__(self) -> None:
        self.human_player = HumanPlayer()
        self.computer_player = ComputerPlayer()
        self.give_card_pack = GiveCardPack()
        self.played_card_pack = PlayedCardPack()
        self.played = False
        self.active_card = False
        self.desired_color = None
        self.stacking = 0
        for _ in range(2):
            for _ in range(2):
                self.take_card(self.human_player)
            for _ in range(2):
                self.take_card(self.computer_player)
        self.played_card_pack.add_card(self.give_card_pack.give_card())

    def run_game(self):
        print("""
              Prsi Card Game
              """)
        while True:
            while not self.played:
                self.print_current_game_state()
                command = input("-> ")
                if command != "exit":
                    self.manage_command(command)

                else:
                    exit(0)
            if not self.human_player.get_card_count():
                print("Victory")
                break
            self.computer_play()
            self.played = False
            if not self.computer_player.get_card_count():
                print("Defeat")
                break

    def manage_command(self, command: str):
        match command.split()[0]:
            case "list_cards":
                self.human_player.list_cards()
            case "play_card":
                if self.play_card(self.human_player, command.split()[1]):
                    self.played = True
                    self.active_card = True
            case "take_card":
                self.take_card(self.human_player)
                self.played = True
                self.active_card = False
            case "stand":
                if self.active_card and self.played_card_pack.last_card()[1] == "a":
                    self.played = True
                    self.active_card = False
                else:
                    print(
                        "You are not playing against an active ace so you cannot stand a round."
                    )
            case _:
                print("Unknown command, use 'help' for list of all available commands.")
        print()

    def take_card(self, player: Player, recursive=False) -> None:
        card = self.give_card_pack.give_card()
        if not card:
            self.give_card_pack.add_cards(self.played_card_pack.give_all_cards())
        if (
            self.active_card
            and not recursive
            and self.played_card_pack.last_card()[1] == "7"
        ):
            for _ in range(1, self.stacking):
                self.take_card(player, True)
            self.stacking = 0
            self.active_card = False
        player.add_card(card)

    def play_card(self, player: Player, card: str) -> bool:
        if player.check_for_card(card):
            if not self.check_card_playable(card):
                print("You cannot play this card now.")
                return False
            player.play_card(card)
            self.desired_color = None
            if card[1] == "m" and type(player) is not ComputerPlayer:
                while True:
                    desired = input("Select the color you want to switch to:")
                    if desired in ["l", "k", "c", "z"]:
                        self.desired_color = desired
                        break
                    else:
                        print("Incorrect color, try again")
            elif card[1] == "7":
                self.stacking += 2
            self.played_card_pack.add_card(card)
            return True
        print(
            "You dont have the card you want to play. Play a different card or take a card."
        )
        return False

    def check_card_playable(self, card) -> bool:
        last_card = self.played_card_pack.last_card()

        if self.active_card:
            match last_card[1]:
                case "7" | "a":
                    return last_card[1] == card[1]
                case "m":
                    if card[0] == self.desired_color or card[1] == "m":
                        return True
                    else:
                        return False
        return (
            (
                (last_card[0] == card[0] or last_card[1] == card[1])
                and self.desired_color is None
            )
            or (card[0] == self.desired_color and self.desired_color is not None)
            or card[1] == "m"
        )

    def print_current_game_state(self):
        print(f"Last played card:\t{self.played_card_pack.last_card()}")
        if self.desired_color:
            print(f"Current color: {self.desired_color}")
        self.human_player.list_cards()
        # print(f"TEST: {', '.join(self.computer_player.card_hand.cards)}")

    def computer_play(self):
        print("Robot turn:")
        playable = self.computer_player.card_hand.cards
        if self.played_card_pack.last_card()[1] == "a" and self.active_card:
            playable = [
                card
                for card in self.computer_player.card_hand.cards
                if card.endswith("a")
            ]
            if not len(playable):
                print("Computer stands a round\n")
                self.active_card = False
                return

        best_move = self.find_best_card(playable, self.played_card_pack.last_card())

        if best_move:
            card, color_choice = best_move
            if card[1] == "m":
                print(f"Computer plays {card} and changes color to {color_choice}")
            else:
                print(f"Computer plays {card}")
            self.play_card(self.computer_player, card)
            self.desired_color = color_choice
            self.played = True
            self.active_card = True
        else:
            print("Computer takes a card.")
            self.take_card(self.computer_player)
            self.played = True
            self.active_card = False
        print()

    def find_best_card(self, cards, last_card):
        """Find the card (and color, if 'm') that can lead to finishing all cards."""

        for card in cards:
            if self.check_card_playable(card):
                remaining = [c for c in cards if c != card]

                if card[1] == "m":
                    for color in ["l", "k", "c", "z"]:
                        if self.can_finish(remaining, (color, "m")):
                            return (card, color)
                else:
                    if self.can_finish(remaining, card):
                        return (card, None)

        for card in cards:
            if self.check_card_playable(card):
                if card[1] == "m":
                    color_counts = {c: 0 for c in ["l", "k", "c", "z"]}
                    for c in cards:
                        if c[0] in color_counts:
                            color_counts[c[0]] += 1
                    best_color = max(color_counts.items(), key=operator.itemgetter(1))[
                        0
                    ]
                    return (card, best_color)
                else:
                    return (card, None)

        return None

    def can_finish(self, remaining_cards, last_card):
        """Return True if it's possible to play all remaining cards (in some order)."""
        if not remaining_cards:
            return True

        for card in remaining_cards:
            if self._is_playable_sim(card, last_card):
                new_hand = [c for c in remaining_cards if c != card]

                if card[1] == "m":
                    for color in ["l", "k", "c", "z"]:
                        if self.can_finish(new_hand, (color, "m")):
                            return True
                else:
                    if self.can_finish(new_hand, card):
                        return True

        return False

    def _is_playable_sim(self, card, last_card):
        """Lightweight version of card-play rules, without state changes."""

        if last_card[1] == "m":
            return card[0] == last_card[0] or card[1] == "m"

        if last_card[1] in ["7", "a"]:
            return card[1] == last_card[1]

        return card[0] == last_card[0] or card[1] == last_card[1] or card[1] == "m"
