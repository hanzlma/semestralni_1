from collections import Counter
import itertools as i
from player import Player, HumanPlayer, ComputerPlayer
from cards import GiveCardPack, PlayedCardPack


class GameRunner:
    """
    Class for managing the game run.

    Attributes:
        human_player (HumanPlayer)
        computer_player (ComputerPlayer)
        give_card_pack (GiveCardPack): Card pack for taking cards.
        played_card_pack (PlayedCardPack): Card pack for played cards.
        played (bool): True if the last turn was made by the human player else False.
        active_card (bool): True if the last card played was active and the effect is affecting the current player else False.
        desired_color (str | None): The color the player switched to with an "*m" card.
        stacking (int): The stacking of taking cards after "*7" cards were played.
    """

    def __init__(self) -> None:
        """Initializes the GameRunner object with all its attributes and gives the starting amount of cards to players."""
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

    def select_difficulty(self) -> None:
        """Selects the game difficulty."""
        inp = ""
        while inp not in ["Easy", "easy", "Hard", "hard", "e", "h"]:
            inp = input("Select difficulty (Easy / Hard): ")
            if inp not in ["Easy", "easy", "Hard", "hard", "e", "h"]:
                print("Incorrect input.\n")
        if inp in ["Easy", "easy", "e"]:
            self.easy = True
        else:
            self.easy = False
        print()

    def run_game(self):
        """Main runner function. Runs the game loop."""
        print("""
              Prsi Card Game
              """)
        self.select_difficulty()
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
        """
        Manages command logic.

        Args:
            command (str): Inputed command.
        """
        try:
            match command.split()[0]:
                case "list_cards" | "lc":
                    self.human_player.list_cards()

                case "play_card" | "pc":
                    if self.play_card(self.human_player, command.split()[1]):
                        self.played = True
                        self.active_card = True

                case "take_card" | "tc":
                    if self.active_card and self.played_card_pack.last_card()[1] == "a":
                        print("\nYou cannot take a card right now.\n")
                        return
                    self.take_card(self.human_player)
                    self.played = True
                    self.active_card = False

                case "help" | "h":
                    print("""
Available commands:
    - list_cards ... lists all cards the player has in his hand
    - play_card <card> ... plays the card if can be played, otherwise it says that it is unplayable
    - take_card ... takes a card from the card deck and adds it to player's hand
    - card_info ... describes all card colours and types
    - help ... shows all commands
    - stand_round ... stands a round (can be only played if you are playing into an ace card)
    - exit ... exits the program
                      """)

                case "stand_round" | "sr":
                    if self.active_card and self.played_card_pack.last_card()[1] == "a":
                        self.played = True
                        self.active_card = False
                    else:
                        print(
                            "You are not playing against an active ace so you cannot stand a round."
                        )

                case "card_info" | "ci":
                    print("""
Card colors: l, k, c, z
Card values:
    - a ... ace
    - 7
    - 8
    - 9
    - 10
    - k
    - m ... color changer
    - s
""")

                case _:
                    print(
                        "Unknown command, use 'help' for list of all available commands."
                    )
        except Exception:
            pass
        print()

    def take_card(self, player: Player, recursive=False) -> None:
        """
        Takes a card from give_card_pack and gives it to the player

        Args:
            player (Player): Player that is taking the card.
            recursive (bool, optional): Recursive call for taking multiple cards. Defaults to False.
        """
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
        """
        Plays a card.

        Args:
            player (Player): Player that is playing the card
            card (str): The card to be played.

        Returns:
            bool: Succes.
        """
        if player.check_for_card(card):
            if not self.check_card_playable(card):
                print("You cannot play this card now.")
                return False
            player.play_card(card)
            self.desired_color = None
            if card[1] == "m" and type(player) is not ComputerPlayer:
                while True:
                    desired = input("Select the color you want to switch to: ")
                    if desired in ["l", "k", "c", "z"]:
                        self.desired_color = desired
                        break
                    else:
                        print("Incorrect color, try again.")
            elif card[1] == "7":
                self.stacking += 2
            self.played_card_pack.add_card(card)
            return True
        print(
            "You dont have the card you want to play. Play a different card or take a card."
        )
        return False

    def check_card_playable(self, card) -> bool:
        """Checks if card is playable. Returns True if playable."""
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
        """Prints current game state."""
        print(f"Last played card:\t{self.played_card_pack.last_card()}")
        if self.desired_color:
            print(f"Current color: {self.desired_color}")
        self.human_player.list_cards()
        # print(f"TEST: {', '.join(self.computer_player.card_hand.cards)}")

    def computer_play(self):
        """Main method of computer player turn logic."""
        print("Robot turn:")

        comp_hand = self.computer_player.card_hand.cards[:]
        human_hands = (
            list(
                [
                    list(c)
                    for c in i.combinations(
                        self.human_player.card_hand.cards[:]
                        + list(self.give_card_pack.cards)[:],
                        self.human_player.get_card_count(),
                    )
                ]
            )
            if self.easy
            else [self.human_player.card_hand.cards[:]]
        )
        print(len(human_hands))
        suggested_moves = []
        for human_hand in human_hands:
            physical_card = self.played_card_pack.last_card()

            if physical_card[1] == "m" and self.desired_color:
                current_card = (self.desired_color, "m")
            else:
                current_card = physical_card

            is_active = self.active_card

            _, move = self.minimax(
                comp_hand,
                human_hand,
                current_card,
                is_active,
                depth=4,
                is_maximizing=True,
            )
            suggested_moves.append(move)
        move = None
        if suggested_moves:
            vote_counts = Counter(suggested_moves)
            best_move_tuple = vote_counts.most_common(1)[0]
            move = best_move_tuple[0]
        if move:
            card, color_choice = move
            if card[1] == "m":
                print(f"Computer plays {card} and changes color to {color_choice}")
            else:
                print(f"Computer plays {card}")

            self.play_card(self.computer_player, card)

            if color_choice:
                self.desired_color = color_choice

            self.played = True
            self.active_card = True if card[1] in ["a", "7"] else False
        else:
            if current_card[1] == "a" and is_active:
                print("Computer stands a round\n")
                self.active_card = False
                return

            print("Computer takes a card.")
            self.take_card(self.computer_player)
            self.played = True
            self.active_card = False
        print()

    def minimax(
        self,
        comp_hand: list[str],
        human_hand: list[str],
        last_card: str,
        is_active: bool,
        depth: int,
        is_maximizing: bool,
        alpha=float("-inf"),
        beta=float("inf"),
    ):
        """
        Minimax implementation for Computer play with Alpha-Beta pruning.

        Args:
            comp_hand (list[str]): Cards in computer player's hand.
            human_hand (list[str]): Cards in human players's hand.
            last_card (str): Last played card.
            is_active (bool): Was last card an active card? True if yes.
            depth (int): How deep should the minimax go.
            is_maximizing (bool): Who is currently playing. True if computer.
            alpha (_type_, optional): Maximum pruning value. Defaults to float("-inf").
            beta (_type_, optional): Minimum pruning value. Defaults to float("inf").

        Returns:
            (score, best_move_tuple)
        """
        if not comp_hand:
            return 100, None
        if not human_hand:
            return -100, None
        if depth == 0:
            return self.evaluate_state(comp_hand, human_hand), None

        current_hand = comp_hand if is_maximizing else human_hand

        moves = self._get_valid_moves(current_hand, last_card, is_active, is_maximizing)

        if not moves:
            if is_active and last_card[1] == "a":
                val, _ = self.minimax(
                    comp_hand,
                    human_hand,
                    last_card,
                    False,
                    depth - 1,
                    not is_maximizing,
                    alpha,
                    beta,
                )
                return val, None
            else:
                penalty = -10 if is_maximizing else 10
                return self.evaluate_state(comp_hand, human_hand) + penalty, None

        best_move = None

        if is_maximizing:
            max_eval = float("-inf")
            for card, color_choice in moves:
                new_hand = [c for c in comp_hand if c != card]
                next_card = (color_choice, "m") if card[1] == "m" else card
                next_active = True if card[1] in ["a", "7"] else False

                eval_score, _ = self.minimax(
                    new_hand,
                    human_hand,
                    next_card,
                    next_active,
                    depth - 1,
                    False,
                    alpha,
                    beta,
                )

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (card, color_choice)

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float("inf")
            for card, color_choice in moves:
                new_hand = [c for c in human_hand if c != card]

                next_card = (color_choice, "m") if card[1] == "m" else card
                next_active = True if card[1] in ["a", "7"] else False

                eval_score, _ = self.minimax(
                    comp_hand,
                    new_hand,
                    next_card,
                    next_active,
                    depth - 1,
                    True,
                    alpha,
                    beta,
                )

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (card, color_choice)

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_state(self, comp_hand: list[str], human_hand: list[str]):
        """Heuristic: Robot wants small hand, Human wants large hand."""
        return len(human_hand) - len(comp_hand)

    def _get_valid_moves(
        self,
        hand: list[str],
        last_card: str,
        is_active: bool,
        computer_turn: bool = False,
    ):
        """Generates all possible moves. Returns list of tuples (card, color_choice)."""
        valid_moves = []

        if is_active and last_card[1] == "7":
            playable = [c for c in hand if c.endswith("7")]

        elif is_active and last_card[1] == "a":
            playable = [c for c in hand if c.endswith("a")]

        else:
            playable = [c for c in hand if self._is_playable_sim(c, last_card)]

        for card in playable:
            if card[1] == "m":
                # If playing 'm', try all suitable colors
                valid_colors = ["l", "k", "c", "z"]
                suitable_colors = []
                if computer_turn:
                    suitable_colors = {c[0] for c in hand if c != card and c[1] != "m"}

                if suitable_colors:
                    valid_colors = list(suitable_colors)

                for color in valid_colors:
                    valid_moves.append((card, color))
            else:
                valid_moves.append((card, None))

        return valid_moves

    def _is_playable_sim(self, card, last_card):
        """Lightweight version of card-play rules, without state changes."""

        if last_card[1] == "m":
            return card[0] == last_card[0] or card[1] == "m"

        return card[0] == last_card[0] or card[1] == last_card[1] or card[1] == "m"
