import unittest

from board import FieldColor
from player import Team, Player, PlayerLocation


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        team_bg = Team("GreenBlue")
        player_north = Player("Green", FieldColor.GREEN, team_bg, PlayerLocation.NORTH)
        player_south = Player("Blue", FieldColor.BLUE, team_bg, PlayerLocation.SOUTH)
        team_bg.players.append(player_north)
        team_bg.players.append(player_south)
        team_ry = Team("RedYellow")
        player_east = Player("Red", FieldColor.RED, team_ry, PlayerLocation.EAST)
        player_west = Player("Yellow", FieldColor.YELLOW, team_ry, PlayerLocation.WEST)
        team_ry.players.append(player_east)
        team_ry.players.append(player_west)
        self.players = [player_north, player_east, player_south, player_west]



if __name__ == '__main__':
    unittest.main()
