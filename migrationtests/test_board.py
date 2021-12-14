import unittest

from board import Board, FieldColor, BoardState
from player import Player, Team, PlayerLocation


class TestBoard(unittest.TestCase):
    """Test the board."""

    def setUp(self) -> None:
        """Setup the board."""
        player_north = Player("Green", FieldColor.GREEN, PlayerLocation.NORTH)
        player_east = Player("Red", FieldColor.RED, PlayerLocation.EAST)
        player_south = Player("Blue", FieldColor.BLUE, PlayerLocation.SOUTH)
        player_west = Player("Yellow", FieldColor.YELLOW, PlayerLocation.WEST)
        Team("GreenBlue", [player_north, player_south])
        Team("RedYellow", [player_east, player_west])
        self.players = [player_north, player_east, player_south, player_west]
        self.board = Board(self.players)
        self.fields_with_marbles = BoardState.get_initial_board_state(self.board.marbles, self.board.waitFields)

    def test_create_marbles(self):
        self.assertTrue(len(self.board.marbles) == 16)
        self.assertTrue(len(self.board.get_marbles_with_color(FieldColor.GREEN)) == 4)
        self.assertTrue(len(self.board.get_marbles_with_color(FieldColor.RED)) == 4)
        self.assertTrue(len(self.board.get_marbles_with_color(FieldColor.BLUE)) == 4)
        self.assertTrue(len(self.board.get_marbles_with_color(FieldColor.YELLOW)) == 4)

    def test_create_fields(self):
        self.assertTrue(len(self.board.fields) == 96)
        self.assertTrue(len(self.board.waitFields) == 16)
        self.assertTrue(len([field for field in self.board.waitFields if field.color_ == FieldColor.GREEN]) == 4)
        self.assertTrue(len(self.board.startFields) == 4)
        self.assertTrue(len([field for field in self.board.startFields if field.color_ == FieldColor.BLUE]) == 1)
        self.assertTrue(len(self.board.homeFields) == 16)
        self.assertTrue(len([field for field in self.board.waitFields if field.color_ == FieldColor.RED]) == 4)

    def test_create_fields_wait_fields(self):
        # Wait fields have no previous and next fields
        self.assertEqual(16, len([field for field in self.board.waitFields if not field.next_fields]))
        self.assertEqual(16, len([field for field in self.board.waitFields if not field.previous_fields]))

    def test_create_fields_start_fields(self):
        self.assertEqual(4, len([field for field in self.board.startFields if len(field.next_fields) == 1]))
        self.assertEqual(4, len([field for field in self.board.startFields if len(field.previous_fields) == 1]))
        # The 4 fields between start and home have 2 next fields
        self.assertEqual(2, len(self.board.fields[4].next_fields))
        self.assertEqual(2, len(self.board.fields[28].next_fields))
        self.assertEqual(2, len(self.board.fields[52].next_fields))
        self.assertEqual(2, len(self.board.fields[76].next_fields))

    def test_create_fields_home_fields(self):
        self.assertEqual(12, len([field for field in self.board.homeFields if len(field.next_fields) == 1]))
        self.assertEqual(16, len([field for field in self.board.homeFields if len(field.previous_fields) == 1]))
        # The 4 fields between start and home have 2 next fields
        self.assertEqual(1, len(self.board.fields[3].next_fields))
        self.assertEqual(1, len(self.board.fields[2].next_fields))
        self.assertEqual(1, len(self.board.fields[1].next_fields))
        self.assertEqual(0, len(self.board.fields[0].next_fields))

    def test_get_start_field_with_color(self):
        self.assertEqual(5, self.board.get_start_field_with_color(FieldColor.GREEN).id_)
        self.assertEqual(29, self.board.get_start_field_with_color(FieldColor.RED).id_)
        self.assertEqual(53, self.board.get_start_field_with_color(FieldColor.BLUE).id_)
        self.assertEqual(77, self.board.get_start_field_with_color(FieldColor.YELLOW).id_)

    def test_get_last_home_field_with_color(self):
        self.assertEqual(0, self.board.get_last_home_field_with_color(FieldColor.GREEN).id_)
        self.assertEqual(24, self.board.get_last_home_field_with_color(FieldColor.RED).id_)
        self.assertEqual(48, self.board.get_last_home_field_with_color(FieldColor.BLUE).id_)
        self.assertEqual(72, self.board.get_last_home_field_with_color(FieldColor.YELLOW).id_)

    def test_get_empty_wait_field_with_color(self):
        self.assertEqual(None, self.board.get_empty_wait_field_with_color(FieldColor.GREEN, self.fields_with_marbles))
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
        BoardState.put_marble_on_field(green_marble, self.board.fields[5], self.fields_with_marbles)
        self.assertEqual(20, self.board.get_empty_wait_field_with_color(FieldColor.GREEN, self.fields_with_marbles).id_)
        # Same test after reset()
        BoardState.reset(self.board, self.fields_with_marbles)
        self.assertEqual(None, self.board.get_empty_wait_field_with_color(FieldColor.GREEN, self.fields_with_marbles))
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
        BoardState.put_marble_on_field(green_marble, self.board.fields[5], self.fields_with_marbles)
        self.assertEqual(20, self.board.get_empty_wait_field_with_color(FieldColor.GREEN, self.fields_with_marbles).id_)

    def test_is_color_finished(self):
        self.assertEqual(False, self.board.is_color_finished(FieldColor.BLUE, self.fields_with_marbles))
        i = 0
        for blue_marble in self.board.get_marbles_with_color(FieldColor.BLUE):
            BoardState.put_marble_on_field(blue_marble, self.board.fields[i], self.fields_with_marbles)
            i += 1
        self.assertEqual(True, self.board.is_color_finished(FieldColor.BLUE, self.fields_with_marbles))
        blue_marble = self.board.get_marbles_with_color(FieldColor.BLUE)[0]
        BoardState.put_marble_on_field(blue_marble, self.board.fields[52], self.fields_with_marbles)
        self.assertEqual(False, self.board.is_color_finished(FieldColor.BLUE, self.fields_with_marbles))

    def test_get_path_for_marble(self):
        blue_marble = self.board.get_marbles_with_color(FieldColor.BLUE)[0]
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
        # No path for marble on WAIT field
        self.assertEqual([], self.board.get_path_for_marble(blue_marble, 10, self.fields_with_marbles))
        # Marble on start, 10 steps
        BoardState.put_marble_on_field(blue_marble, self.board.fields[53], self.fields_with_marbles)
        self.assertEqual(self.board.fields[54:64], self.board.get_path_for_marble(blue_marble, 10, self.fields_with_marbles))
        # Marble -4 steps
        BoardState.put_marble_on_field(blue_marble, self.board.fields[52], self.fields_with_marbles)
        self.assertListEqual(list(reversed(self.board.fields[40:44])),
                             self.board.get_path_for_marble(blue_marble, -4, self.fields_with_marbles))
        # Blue marble on start, test path for green marble
        BoardState.put_marble_on_field(blue_marble, self.board.fields[53], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marble, self.board.fields[42], self.fields_with_marbles)
        self.assertListEqual([self.board.fields[43], self.board.fields[52]],
                             self.board.get_path_for_marble(green_marble, 2, self.fields_with_marbles))
        # Expected path too long --> empty path
        self.assertListEqual([], self.board.get_path_for_marble(green_marble, 3, self.fields_with_marbles))
        # Expected path too long, but get_shorter_path == True --> two fields
        self.assertListEqual([self.board.fields[43], self.board.fields[52]],
                             self.board.get_path_for_marble(green_marble, 3, self.fields_with_marbles, True))
        # Blue marble running home
        blue_marble2 = self.board.get_marbles_with_color(FieldColor.BLUE)[1]
        BoardState.put_marble_on_field(blue_marble2, self.board.fields[43], self.fields_with_marbles)
        self.assertListEqual(list(reversed(self.board.fields[48:53])),
                             self.board.get_path_for_marble(blue_marble2, 5, self.fields_with_marbles))
        BoardState.put_marble_on_field(blue_marble2, self.board.fields[52], self.fields_with_marbles)
        self.assertListEqual([], self.board.get_path_for_marble(blue_marble2, 5, self.fields_with_marbles))

    # def test_set_fields_with_marbles(self):
    #     new_fields_with_marbles = dict(self.fields_with_marbles)
    #     blue_marble = self.board.get_marbles_with_color(FieldColor.BLUE)[0]
    #     green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
    #     BoardState.put_marble_on_field(blue_marble, self.board.fields[53], self.fields_with_marbles)
    #     self.assertEqual(blue_marble, BoardState.get_marble_for_field(self.board.fields[53]), self.fields_with_marbles)
    #     self.assertEqual(self.board.fields[53], BoardState.get_field_for_marble(blue_marble), self.fields_with_marbles)
    #     self.assertEqual(green_marble, BoardState.get_marble_for_field(self.board.fields[20]), self.fields_with_marbles)
    #     self.assertEqual(self.board.fields[20], BoardState.get_field_for_marble(green_marble), self.fields_with_marbles)
    #     # Set the board_state
    #     self.board_state.set_fields_with_marbles(new_fields_with_marbles)
    #     self.assertEqual(None, self.board_state.get_marble_for_field_opt(self.board.fields[53]))
    #     self.assertEqual(self.board.fields[68], self.board_state.get_field_for_marble(blue_marble))
    #     self.assertEqual(green_marble, self.board_state.get_marble_for_field(self.board.fields[20]))
    #     self.assertEqual(self.board.fields[20], self.board_state.get_field_for_marble(green_marble))

    def test_get_board_state_as_array(self):
        array = BoardState.get_board_state_as_array(self.fields_with_marbles, self.board, self.players)
        self.assertEqual(96, len(array))
        self.assertEqual(1, array[20])
        self.assertEqual(2, array[44])
        self.assertEqual(3, array[68])
        self.assertEqual(4, array[92])

if __name__ == '__main__':
    unittest.main()
