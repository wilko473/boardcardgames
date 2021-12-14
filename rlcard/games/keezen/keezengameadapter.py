import numpy as np
from rlcard.games.keezen.board import FieldColor, Board
from rlcard.games.keezen.game import Game, GameActions
from rlcard.games.keezen.player import Player, PlayerLocation, Team
from rlcard.games.keezen.rules import Rules


class KeezenGameAdapter:
    """Adapter class to use the Keezen game in RLCard. The state and actions are converted to dict and ints."""

    game_type = "Keez"  # "KeezSimple"  # or "Keez"

    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        player_north = Player("Green", FieldColor.GREEN, PlayerLocation.NORTH)
        player_east = Player("Red", FieldColor.RED, PlayerLocation.EAST)
        player_south = Player("Blue", FieldColor.BLUE, PlayerLocation.SOUTH)
        player_west = Player("Yellow", FieldColor.YELLOW, PlayerLocation.WEST)
        self.players = [player_north, player_east, player_south, player_west]
        self.team_bg = Team("GreenBlue", [player_north, player_south])
        self.team_ry = Team("RedYellow", [player_east, player_west])

        self.game = Game(Rules(KeezenGameAdapter.game_type), self.players, Board(self.players))
        self.game_state = None

        self._ACTION_SPACE = {}  # [action_id: action_index] for example: ("RU01P0": 2)
        idx = 0
        if self.game.rules.game_type == "Keez":
            for action_id in GameActions.ALL_ACTIONS_271:
                self._ACTION_SPACE[action_id] = idx
                idx += 1
        elif self.game.rules.game_type == "KeezSimple":
            for action_id in GameActions.ALL_ACTIONS_SIMPLE:
                self._ACTION_SPACE[action_id] = idx
                idx += 1

    def configure(self, game_config):
        '''Specify some game specific parameters, such as number of players'''
        self.num_players = game_config['game_num_players']

    def init_game(self):
        self.game_state = None
        self.game_state, player_idx = self.game.init_game()
        self.state = self.get_state(player_idx)
        return self.state, player_idx

    def step(self, action):  # action, for example: 'ST13P3'
        """Do a move. Action is the raw id of a move."""
        move = None
        if action != 'NO':
            moves = [move for move in self.game.get_allowed_moves(self.game_state) if
                     move.get_raw_action(self.game, self.game_state) == action]
            move = moves[0]
        self.game_state, rewards, done = self.game.step(move, self.game_state)
        player_idx = self.game.players.index(self.game_state.move_player)

        self.state = self.get_state(player_idx)
        return self.state, player_idx

    def step_back(self):
        prev_game_state = self.game.step_back()
        if prev_game_state:
            self.game_state = prev_game_state
            player_idx = self.game.players.index(self.game_state.move_player)
            player_state = self.get_state(player_idx)
            self.state = player_state
            return player_state, player_idx

    def get_state(self, player_id):
        allowed_moves = self.game.get_allowed_moves(self.game_state)
        if self.is_over():
            actions = []
        else:
            actions = dict(self._get_legal_actions(allowed_moves))
        player_state = self.game_state.get_state_for_player(self.game.players[player_id])
        state = {'legal_actions': actions, 'allowed_moves': allowed_moves, 'game_state': self.game_state,
                 'state_for_player': player_state['state_for_player'],
                 'fields_with_marbles': player_state['fields_with_marbles'],
                 'players_play_with_color': player_state['players_play_with_color']}
        return state

    def get_state_for_current_player(self):
        player_idx = self.game.players.index(self.game_state.move_player)
        return self.get_state(player_idx)

    @staticmethod
    def get_action_num():
        if KeezenGameAdapter.game_type == "KeezSimple":
            return Game.GAME_ACTIONS_SIMPLE
        return Game.GAME_ACTIONS

    def get_player_id(self):
        return self.game.players.index(self.game_state.move_player)

    def get_player_num(self):
        return len(self.game.players)

    def is_over(self):
        done, rewards = self.game.is_over(self.game_state)
        return done

    def render(self):
        self.game.render(self.game_state)

    def _get_legal_actions(self, allowed_moves) -> [int]:
        action_space = self._ACTION_SPACE
        legal_moves = {}  # [action_index: action_matrix]
        for move in allowed_moves:
            raw_action = move.get_raw_action(self.game, self.game_state)
            action_idx = action_space[raw_action]
            action_matrix = move.get_action_matrix(self.game, self.game_state)
            legal_moves[action_idx] = action_matrix
        if not legal_moves:
            no_idx = action_space['NO']
            legal_moves[no_idx] = np.zeros(68, dtype=np.int8)  # pass
        return legal_moves

    def get_num_players(self) -> int:
        return 4


    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions.
        '''
        return len(GameActions.ALL_ACTIONS_271)

