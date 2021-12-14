import numpy as np

from rlcard.games.keezen.board import Field, Marble, BoardState
from rlcard.games.keezen.player import Player


class MoveType:
    START = "START"
    RUN = "RUN"
    SPLIT = "SPLIT"
    THROW_CARDS = "THROW_CARDS"
    SWITCH = "SWITCH"
    DEAL = "DEAL"


class Move:
    """Represents a move of a player, throwing cards and moving marbles."""

    def __init__(self, move_type: MoveType, player: Player, cards, marble_moves):
        """Creates a move."""
        self.move_type = move_type
        self.player = player
        self.cards = cards
        self.marble_moves = marble_moves

    def __str__(self):
        card_zero = ""
        if len(self.cards) > 0:
            card_zero = str(self.cards[0])
        marbles = ""
        for marble_move in self.marble_moves:
            marbles = marbles + "[" + str(marble_move.marble) + ", from:" + str(marble_move.from_field) + ", to:" + str(
                marble_move.to_field) + "]"
        return "Move: {0} by player {1}. card: {2}. marblemoves: ".format(self.move_type, self.player.name, card_zero,
                                                                          marbles)

    def _get_raw_action(self):
        if self.move_type == MoveType.THROW_CARDS:
            return "TC"
        elif self.move_type == MoveType.DEAL:
            return "DL"
        else:
            if self.move_type == MoveType.START:
                return "ST" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                       + str(self.marble_moves[0].marble.raw_id)
            elif self.move_type == MoveType.RUN:
                return "RU" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                       + str(self.marble_moves[0].marble.raw_id)
            elif self.move_type == MoveType.SPLIT:
                result = "SP" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                         + str(self.marble_moves[0].marble.raw_id)
                if len(self.marble_moves) == 2:
                    result += str(len(self.marble_moves[0].steps))
                    if self.marble_moves[0].marble.color_ == self.marble_moves[1].marble.color_:
                        result += "P" + str(self.marble_moves[1].marble.raw_id)
                    elif self.marble_moves[1].marble.color_ == self.player.get_team_mate().player_color:
                        result += "T" + str(self.marble_moves[1].marble.raw_id)
                return result
            elif self.move_type == MoveType.SWITCH:
                result = "SW" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                         + str(self.marble_moves[0].marble.raw_id)
                if len(self.marble_moves) == 2:
                    if self.marble_moves[1].marble.color_ == self.player.get_team_mate().player_color:
                        result += "T" + str(self.marble_moves[1].marble.raw_id)
                    else:
                        result += "O" + str(self.marble_moves[1].marble.raw_id)
                return result

    # Get al actions based on marble positions: P0, P1, P2 and P3 in stead of marble id
    def get_raw_action(self, game, game_state):
        if self.move_type == MoveType.THROW_CARDS:
            return "TC"
        elif self.move_type == MoveType.DEAL:
            return "DL"
        else:
            if self.move_type == MoveType.START:
                return "ST" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                       + str(Move.get_marble_position(game, game_state, self.marble_moves[0].marble))
            elif self.move_type == MoveType.RUN:
                return "RU" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                       + str(Move.get_marble_position(game, game_state, self.marble_moves[0].marble))
            elif self.move_type == MoveType.SPLIT:
                result = "SP" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                         + str(Move.get_marble_position(game, game_state, self.marble_moves[0].marble))
                if len(self.marble_moves) == 2:
                    result += str(len(self.marble_moves[0].steps))
                    if self.marble_moves[0].marble.color_ == self.marble_moves[1].marble.color_:
                        result += "P" + str(Move.get_marble_position(game, game_state, self.marble_moves[1].marble))
                    elif self.marble_moves[1].marble.color_ == self.player.get_team_mate().player_color:
                        result += "T" + str(Move.get_marble_position(game, game_state, self.marble_moves[1].marble))
                return result
            elif self.move_type == MoveType.SWITCH:
                result = "SW" + str(self.cards[0].card_value.value).zfill(2) + "P" \
                         + str(Move.get_marble_position(game, game_state, self.marble_moves[0].marble))
                if len(self.marble_moves) == 2:
                    if self.marble_moves[1].marble.color_ == self.player.get_team_mate().player_color:
                        result += "T" + str(Move.get_marble_position(game, game_state, self.marble_moves[1].marble))
                    else:
                        next_player_color = self.player.get_next_player(game.players).player_color
                        oppo_char = "B"
                        if next_player_color == self.marble_moves[1].marble.color_:
                            oppo_char = "A"
                        result += oppo_char + str(
                            Move.get_marble_position(game, game_state, self.marble_moves[1].marble))
                return result

    def get_action_matrix(self, game, game_state):
        """Returns a matrix representation of this move."""
        # First [13x4]/[52] are the cards, [16] are the affected marbles: 0-3 own (0 is most progress),
        player_color_position = {}
        index_of_player = game.players.index(self.player)
        player_color_position[self.player.player_color] = 0
        for index in range(1, 4):
            index_of_next_player = (index_of_player + index) % len(game.players)
            player_color_position[game.players[index_of_next_player].player_color] = index_of_next_player

        result = np.zeros(68, dtype=np.int8)
        for card in self.cards:
            suit = card.suit
            value = card.card_value
            index = suit*13 + value - 1
            result[index] = 1
        affected_marbles = []
        for marble_move in self.marble_moves:
            affected_marbles.append(marble_move.marble)
            for hit_marble_move in marble_move.hit_marble_moves:
                affected_marbles.append(hit_marble_move.marble)
        for marble in affected_marbles:
            marble_pos = Move.get_marble_position(game, game_state, marble)
            # player pos = 0: own, 1: next player, 2: teammate, 3: other player
            player_pos = player_color_position[marble.color_]
            result[player_pos*4 + marble_pos] = 1
        return result

    @staticmethod
    def get_marble_position(game, game_state, a_marble):
        """Gives the position index of a marble. Most progress == 0, less progress: 1, 2 and last: 3"""
        result = 0
        color_index = 0
        for i in range(len(game.players)):
            if game.players[i].player_color == a_marble.color_:
                color_index = i
        path = BoardState.PATH_FOR_LOCATION[color_index]
        field = BoardState.get_field_for_marble(a_marble, game_state.fields_with_marbles)
        marble_index = path.index(field.id_)
        other_marbles = [marble for marble in game.board.marbles if marble != a_marble
                         and marble.color_ == a_marble.color_]
        for other_marble in other_marbles:
            other_field = BoardState.get_field_for_marble(other_marble, game_state.fields_with_marbles)
            index = path.index(other_field.id_)
            if index > marble_index:
                result += 1
        return result


class MarbleMove:
    """Represents the move of a marble from one field to another.
    This marble move can contain moves of marbles that are hit."""

    def __init__(self, marble: Marble, from_field: Field, to_field: Field, steps: [Field]):
        self.marble = marble
        self.from_field = from_field
        self.to_field = to_field
        self.steps = steps
        self.hit_marble_moves = {}  # The hit marble moves are set during move creation.

    def __str__(self):
        return "Move {0} marble with ID {1} from field {2} to {3}. Hits: {4}.".format(self.marble.color_,
                                                                                      self.marble.id_,
                                                                                      self.from_field.id_,
                                                                                      self.to_field.id_,
                                                                                      len(self.hit_marble_moves))
