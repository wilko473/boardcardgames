import unittest

from board import FieldColor, Board, BoardState
from card import Card, CardValue, Suit
from cardop import CardOpStart, CardOpRun, CardOpSwitchOneOwnMarble, CardOpSplitTwoMarbles
from move import MoveType
from player import Team, Player, PlayerLocation


class TestCardOp(unittest.TestCase):

    def setUp(self) -> None:
        """Setup the board."""
        player_north = Player("Green", FieldColor.GREEN, PlayerLocation.NORTH)
        player_south = Player("Blue", FieldColor.BLUE, PlayerLocation.SOUTH)
        player_east = Player("Red", FieldColor.RED, PlayerLocation.EAST)
        player_west = Player("Yellow", FieldColor.YELLOW, PlayerLocation.WEST)
        Team("GreenBlue", [player_north, player_south])
        Team("RedYellow", [player_east, player_west])
        self.players = [player_north, player_east, player_south, player_west]
        self.board = Board(self.players)
        self.fields_with_marbles = BoardState.get_initial_board_state(self.board.marbles, self.board.waitFields)

    def test_cardop_start(self):
        cardop = CardOpStart(self.board)
        card_king = Card(Suit.CLUBS, CardValue.KING, 13)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card_king, self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        self.assertEqual(MoveType.START, moves[0].move_type)
        self.assertEqual(20, moves[0].marble_moves[0].from_field.id_)
        self.assertEqual(5, moves[0].marble_moves[0].to_field.id_)

    def test_cardop_run(self):
        card10 = Card(Suit.CLUBS, CardValue.TEN, 10)
        cardop = CardOpRun(self.board, 10)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card10, self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
        BoardState.put_marble_on_field(green_marble, self.board.fields[5],
                                       self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card10, self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        self.assertEqual(5, moves[0].marble_moves[0].from_field.id_)
        self.assertEqual(15, moves[0].marble_moves[0].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[0].hit_marble_moves))
        # Put a marble on field 15 that will be hit
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[1]
        BoardState.put_marble_on_field(green_marble, self.board.fields[15], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card10, self.fields_with_marbles)
        self.assertEqual(15, moves[0].marble_moves[0].hit_marble_moves[0].from_field.id_)
        self.assertEqual(20, moves[0].marble_moves[0].hit_marble_moves[0].to_field.id_)

    def test_cardop_switch(self):
        cardop = CardOpSwitchOneOwnMarble(self.board)
        cardJack = Card(Suit.CLUBS, CardValue.JACK, 11)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, cardJack, self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        # Put green and blue marbles on start -> no allowed move expected
        green_marble = self.board.get_marbles_with_color(FieldColor.GREEN)[0]
        BoardState.put_marble_on_field(green_marble, self.board.fields[5], self.fields_with_marbles)
        blue_marble = self.board.get_marbles_with_color(FieldColor.BLUE)[0]
        BoardState.put_marble_on_field(blue_marble, self.board.fields[53], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, cardJack, self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        # Put blue marble on normal field -> expect 1 move
        BoardState.put_marble_on_field(blue_marble, self.board.fields[54], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, cardJack, self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        self.assertEqual(5, moves[0].marble_moves[0].from_field.id_)
        self.assertEqual(54, moves[0].marble_moves[0].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[0].hit_marble_moves))
        self.assertEqual(54, moves[0].marble_moves[1].from_field.id_)
        self.assertEqual(5, moves[0].marble_moves[1].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[1].hit_marble_moves))

    def test_cardop_split_basic(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, Card(Suit.CLUBS, CardValue.SEVEN, 7)
                                 , self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        # Put green marble on start -> one allowed move expected
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[5], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, Card(Suit.CLUBS, CardValue.SEVEN, 7)
                                 , self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        self.assertEqual(5, moves[0].marble_moves[0].from_field.id_)
        self.assertEqual(12, moves[0].marble_moves[0].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[0].hit_marble_moves))
        # Put other green marbles at other start fields -> 40 moves expected
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[29], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[53], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[3], self.board.fields[77], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, Card(Suit.CLUBS, CardValue.SEVEN, 7),
                                 self.fields_with_marbles)
        self.assertEqual(40, len(moves))  # 4x7 + 4X6+1x3 + 4x5+2x3 + 4x4+3x3 = 40

    def test_cardop_split_home(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        card7 = Card(Suit.CLUBS, CardValue.SEVEN, 7)
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        # Put green marble on 1st home, 2nd marble 2 before -> 1 move
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[3], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[91], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        self.assertEqual(3, moves[0].marble_moves[0].from_field.id_)
        self.assertEqual(0, moves[0].marble_moves[0].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[0].hit_marble_moves))
        self.assertEqual(91, moves[0].marble_moves[1].from_field.id_)
        self.assertEqual(1, moves[0].marble_moves[1].to_field.id_)
        self.assertEqual(0, len(moves[0].marble_moves[1].hit_marble_moves))
        # Put green marble between other 2: still 1 move
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[4], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(1, len(moves))
        # Put first green marble back on wait: no move
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[20], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        # Put green marble back on start: 4 moves (1 7x and 3 combined)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[5], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(4, len(moves))
        # Two green marbles in front of home: 4 moves (ma6+mb1,ma5+mb2,ma5+mb2,ma4+mb3)
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[91], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[90], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[20], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[3], self.board.fields[21], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(4, len(moves))

    def test_cardop_split_hit(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        card7 = Card(Suit.CLUBS, CardValue.SEVEN, 7)
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        # Put green marble on start, 2nd marble in hit range -> 8 moves
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[5], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[6], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(8, len(moves))
        # Move 2nd marble one field further
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[7], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(8, len(moves))
        for move in moves:
            if len(move.marble_moves) == 2:
                if move.marble_moves[1].hit_marble_moves:
                    self.assertEqual(7, move.marble_moves[0].from_field.id_)
                    self.assertEqual(12, move.marble_moves[0].to_field.id_)
                    self.assertEqual(0, len(move.marble_moves[0].hit_marble_moves))
                    self.assertEqual(5, move.marble_moves[1].from_field.id_)
                    self.assertEqual(7, move.marble_moves[1].to_field.id_)
                    self.assertEqual(0, len(move.marble_moves[1].hit_marble_moves))

    def test_cardop_split_hit_both(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        card7 = Card(Suit.CLUBS, CardValue.SEVEN, 7)
        blue_marbles = self.board.get_marbles_with_color(FieldColor.BLUE)
        # Put blue marbles at 5 and 2 fields distance to have two hits
        BoardState.put_marble_on_field(blue_marbles[0], self.board.fields[53], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[1], self.board.fields[35], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[2], self.board.fields[40], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[3], self.board.fields[55], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[2], self.players[2].player_color, card7, self.fields_with_marbles)
        hit_test = 0
        for move in moves:
            if len(move.marble_moves) == 2:
                if move.marble_moves[0].hit_marble_moves and move.marble_moves[1].hit_marble_moves:
                    self.assertEqual(35, move.marble_moves[0].from_field.id_)
                    self.assertEqual(40, move.marble_moves[0].to_field.id_)
                    self.assertEqual(1, len(move.marble_moves[0].hit_marble_moves))
                    self.assertEqual(68, move.marble_moves[0].hit_marble_moves[0].to_field.id_)
                    self.assertEqual(53, move.marble_moves[1].from_field.id_)
                    self.assertEqual(55, move.marble_moves[1].to_field.id_)
                    self.assertEqual(1, len(move.marble_moves[1].hit_marble_moves))
                    self.assertEqual(69, move.marble_moves[1].hit_marble_moves[0].to_field.id_)
                    hit_test += 1
        self.assertEqual(1, hit_test)

    def test_cardop_split_hit_both2(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        card7 = Card(Suit.CLUBS, CardValue.SEVEN, 7)
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        blue_marbles = self.board.get_marbles_with_color(FieldColor.BLUE)
        red_marbles = self.board.get_marbles_with_color(FieldColor.RED)
        yellow_marbles = self.board.get_marbles_with_color(FieldColor.YELLOW)
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[0], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[19], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[91], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[3], self.board.fields[11], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[0], self.board.fields[49], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[1], self.board.fields[4], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[2], self.board.fields[17], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[3], self.board.fields[68], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[0], self.board.fields[24], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[1], self.board.fields[43], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[2], self.board.fields[67], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[3], self.board.fields[29], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[0], self.board.fields[72], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[1], self.board.fields[92], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[2], self.board.fields[74], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[3], self.board.fields[93], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        hit_test = 0
        for move in moves:
            if len(move.marble_moves) == 2:
                if move.marble_moves[0].hit_marble_moves and move.marble_moves[1].hit_marble_moves:
                    self.assertEqual(11, move.marble_moves[0].from_field.id_)
                    self.assertEqual(17, move.marble_moves[0].to_field.id_)
                    self.assertEqual(1, len(move.marble_moves[0].hit_marble_moves))
                    self.assertEqual(69, move.marble_moves[0].hit_marble_moves[0].to_field.id_)
                    self.assertEqual(91, move.marble_moves[1].from_field.id_)
                    self.assertEqual(4, move.marble_moves[1].to_field.id_)
                    self.assertEqual(1, len(move.marble_moves[1].hit_marble_moves))
                    self.assertEqual(70, move.marble_moves[1].hit_marble_moves[0].to_field.id_)
                    hit_test += 1
        self.assertEqual(1, hit_test)

    def test_cardop_split_switchcolor(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        card7 = Card(Suit.CLUBS, CardValue.SEVEN, 7)
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        # Put 3 green marbles on home, 4th marble to finish -> No move without team mate moves
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[0], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[1], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[2], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[3], self.board.fields[89], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(0, len(moves))
        # Put team mate marbles -> 2 moves
        blue_marbles = self.board.get_marbles_with_color(FieldColor.BLUE)
        BoardState.put_marble_on_field(blue_marbles[0], self.board.fields[51], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[1], self.board.fields[53], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[0], self.players[0].player_color, card7, self.fields_with_marbles)
        self.assertEqual(2, len(moves))

    def test_cardop_split_all(self):
        cardop = CardOpSplitTwoMarbles(self.board)
        blue_marbles = self.board.get_marbles_with_color(FieldColor.BLUE)
        # Put blue marbles at start fields -> 40 moves expected
        BoardState.put_marble_on_field(blue_marbles[0], self.board.fields[5], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[1], self.board.fields[29], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[2], self.board.fields[53], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[3], self.board.fields[77], self.fields_with_marbles)
        moves = cardop.get_moves(self.players[2], self.players[2].player_color, Card(Suit.CLUBS, CardValue.SEVEN, 7),
                                 self.fields_with_marbles)
        self.assertEqual(40, len(moves))  # 4x7 + 4X6+1x3 + 4x5+2x3 + 4x4+3x3 = 40

    def test_cardop_switch_all(self):
        cardop = CardOpSwitchOneOwnMarble(self.board)
        # Put all marbles on board at switchable positions
        green_marbles = self.board.get_marbles_with_color(FieldColor.GREEN)
        BoardState.put_marble_on_field(green_marbles[0], self.board.fields[6], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[1], self.board.fields[7], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[2], self.board.fields[8], self.fields_with_marbles)
        BoardState.put_marble_on_field(green_marbles[3], self.board.fields[9], self.fields_with_marbles)
        red_marbles = self.board.get_marbles_with_color(FieldColor.RED)
        BoardState.put_marble_on_field(red_marbles[0], self.board.fields[30], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[1], self.board.fields[31], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[2], self.board.fields[32], self.fields_with_marbles)
        BoardState.put_marble_on_field(red_marbles[3], self.board.fields[33], self.fields_with_marbles)
        blue_marbles = self.board.get_marbles_with_color(FieldColor.BLUE)
        BoardState.put_marble_on_field(blue_marbles[0], self.board.fields[54], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[1], self.board.fields[55], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[2], self.board.fields[56], self.fields_with_marbles)
        BoardState.put_marble_on_field(blue_marbles[3], self.board.fields[57], self.fields_with_marbles)
        yellow_marbles = self.board.get_marbles_with_color(FieldColor.YELLOW)
        BoardState.put_marble_on_field(yellow_marbles[0], self.board.fields[78], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[1], self.board.fields[79], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[2], self.board.fields[80], self.fields_with_marbles)
        BoardState.put_marble_on_field(yellow_marbles[3], self.board.fields[81], self.fields_with_marbles)

        moves = cardop.get_moves(self.players[2], self.players[2].player_color, Card(Suit.CLUBS, CardValue.JACK, 1)
                                 , self.fields_with_marbles)
        self.assertEqual(48, len(moves))
        for move in moves:
            print('"' + move.raw_action + '",')


if __name__ == '__main__':
    unittest.main()
