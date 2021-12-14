import unittest

from board import FieldColor
from card import CardState
from player import Team, Player, PlayerLocation
from rules import Rules


class TestCard(unittest.TestCase):

    def setUp(self) -> None:
        player_north = Player("Green", FieldColor.GREEN, PlayerLocation.NORTH)
        player_south = Player("Blue", FieldColor.BLUE, PlayerLocation.SOUTH)
        player_east = Player("Red", FieldColor.RED, PlayerLocation.EAST)
        player_west = Player("Yellow", FieldColor.YELLOW, PlayerLocation.WEST)
        Team("GreenBlue", [player_north, player_south])
        Team("RedYellow", [player_east, player_west])
        self.players = [player_north, player_east, player_south, player_west]
        self.cards = Rules.initialize_cards()
        self.stock_cards, self.player_cards, self.played_cards = CardState.get_initial_card_state(self.cards,
                                                                                                  self.players)

    def test_card_position_int(self):
        self.assertEqual(52, len(self.stock_cards))
        self.assertEqual([], self.played_cards)
        for i in range(4):
            self.assertEqual([], self.player_cards[self.players[i]])

    def test_deal_card(self):
        CardState.deal_card(self.players[0], self.stock_cards, self.player_cards)
        self.assertEqual(51, len(self.stock_cards))
        self.assertEqual(1, len(self.player_cards[self.players[0]]))
        self.assertEqual(0, len(self.played_cards))

    def test_play_cards(self):
        CardState.deal_card(self.players[0], self.stock_cards, self.player_cards)
        CardState.deal_card(self.players[0], self.stock_cards, self.player_cards)
        self.assertEqual(50, len(self.stock_cards))
        self.assertEqual(2, len(self.player_cards[self.players[0]]))
        self.assertEqual(0, len(self.played_cards))
        CardState.play_cards(self.players[0], self.player_cards[self.players[0]], self.player_cards, self.played_cards)
        self.assertEqual(50, len(self.stock_cards))
        self.assertEqual(0, len(self.player_cards[self.players[0]]))
        self.assertEqual(2, len(self.played_cards))
        CardState.reset(self.stock_cards, self.player_cards, self.played_cards)
        self.assertEqual(52, len(self.stock_cards))
        self.assertEqual(0, len(self.player_cards[self.players[0]]))
        self.assertEqual(0, len(self.played_cards))

    def test_get_card_state_as_array(self):
        array = CardState.get_card_state_as_array(self.players[0], self.players, self.cards, self.stock_cards,
                                                  self.player_cards, self.played_cards)
        self.assertEqual(96, len(array))
        self.assertEqual(0, array[56])  # played cards
        self.assertEqual(52, array[57])  # Stock cards

if __name__ == '__main__':
    unittest.main()
