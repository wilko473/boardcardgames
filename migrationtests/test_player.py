import unittest

from board import FieldColor
from player import Player, PlayerLocation, Team


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        player_north = Player("Green", FieldColor.GREEN, PlayerLocation.NORTH)
        player_south = Player("Blue", FieldColor.BLUE, PlayerLocation.SOUTH)
        player_east = Player("Red", FieldColor.RED, PlayerLocation.EAST)
        player_west = Player("Yellow", FieldColor.YELLOW, PlayerLocation.WEST)
        Team("GreenBlue", [player_north, player_south])
        Team("RedYellow", [player_east, player_west])
        self.players = [player_north, player_east, player_south, player_west]

    def test_get_next_player(self):
        self.assertEqual(self.players[1], self.players[0].get_next_player(self.players))
        self.assertEqual(self.players[2], self.players[1].get_next_player(self.players))
        self.assertEqual(self.players[3], self.players[2].get_next_player(self.players))
        self.assertEqual(self.players[0], self.players[3].get_next_player(self.players))

    def test_get_team_mate(self):
        self.assertEqual(self.players[0], self.players[2].get_team_mate())
        self.assertEqual(self.players[1], self.players[3].get_team_mate())
        self.assertEqual(self.players[2], self.players[0].get_team_mate())
        self.assertEqual(self.players[3], self.players[1].get_team_mate())

if __name__ == '__main__':
    unittest.main()
