from collections import OrderedDict
import numpy as np
from rlcard.envs import Env
from rlcard.games.keezen.board import BoardState
from rlcard.games.keezen.card import CardState
from rlcard.games.keezen.game import GameActions
from rlcard.games.keezen.keezengameadapter import KeezenGameAdapter

DEFAULT_GAME_CONFIG = {
        'game_num_players': 4,
        }


class KeezenEnv(Env):
    """ Keezen Environment."""

    def __init__(self, config):
        self.name = 'keezen'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = KeezenGameAdapter()
        self.action_num = self.game.get_action_num()
        self._ACTION_LIST = []  # List with all action ids, such as 'NO','DL','RU01P0','RO01P1' etc
        self._ACTION_SPACE = {}  # Map action indexes to action ids String (action id) --> int (action index)
        idx = 0
        if self.game.game.rules.game_type == "Keez":
            self._ACTION_LIST = GameActions.ALL_ACTIONS_271
            for action_id in self._ACTION_LIST:
                self._ACTION_SPACE[action_id] = idx
                idx += 1
        elif self.game.game.rules.game_type == "KeezSimple":
            self._ACTION_LIST = GameActions.ALL_ACTIONS_SIMPLE
            for action_id in self._ACTION_LIST:
                self._ACTION_SPACE[action_id] = idx
                idx += 1
        super().__init__(config)

        self.state_shape = [[615], [615], [615], [615]]
        self.action_shape = [[68] for _ in range(self.num_players)]
        self.raw_legal_actions = {}
        for i in range(len(GameActions.ALL_ACTIONS_271)):
            self.raw_legal_actions[i] = GameActions.ALL_ACTIONS_271[i]

    def _extract_state(self, state):
        fields_with_marbles = state['fields_with_marbles']
        cur_player = state['state_for_player']
        play_with_color = state['players_play_with_color']

        cur_player_plays_with_color = play_with_color[cur_player]
        own_cards = CardState.get_card_state_as_matrix(self.game.game_state.player_cards[cur_player])
        played_cards = CardState.get_card_state_as_matrix(self.game.game_state.played_cards)
        board_matrix = BoardState.get_board_state_as_matrix(fields_with_marbles, self.game.game.board, cur_player,
                                                            cur_player_plays_with_color, self.game.game.players)
        active_player = np.zeros(5, dtype=np.int8)
        index_of_cur_player = self.game.game.players.index(cur_player)
        active_player[index_of_cur_player] = 1
        extracted_state = OrderedDict({'obs': np.concatenate((active_player, own_cards, played_cards, board_matrix)),
                                       'player_id': self.game.game.players.index(cur_player),
                                       'legal_actions': self._get_legal_actions(),
                                       'allowed_moves': state.get("allowed_moves"),
                                       'action_record': self.action_recorder,
                                       'raw_legal_actions': self.raw_legal_actions})
        extracted_state['game_state'] = state['game_state']
        return extracted_state

    def get_payoffs(self):
        """ Get the payoffs of players. Returns: payoffs (list): a list of payoffs for each player"""
        is_over, rewards = self.game.game.is_over(self.game.game_state)
        if not is_over:
            return None
        payoffs = np.array([0, 0, 0, 0])
        i = 0
        for reward in rewards:
            payoffs[i] = reward
            i += 1
        return payoffs

    def _decode_action(self, action_idx):
        """ Action id -> the action in the game ('ST13P0', 'TC', ...)."""
        action_id = self._ACTION_LIST[action_idx]
        return action_id

    def _get_legal_actions(self):
        """ Get all legal actions (idx and matrix) for current state."""
        legal_actions = self.game.get_state_for_current_player()["legal_actions"]
        return legal_actions

