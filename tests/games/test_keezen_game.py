import unittest
import numpy as np

from rlcard.games.keezen.game import GameActions
from rlcard.games.keezen.keezengameadapter import KeezenGameAdapter


class TestKeezenMethods(unittest.TestCase):

    def test_get_player_num(self):
        game = KeezenGameAdapter()
        num_player = game.get_player_num()
        self.assertEqual(num_player, 4)

    def test_get_action_num(self):
        game = KeezenGameAdapter()
        action_num = game.get_action_num()
        self.assertEqual(action_num, 271)

    def test_init_game(self):
        game = KeezenGameAdapter()
        state, _ = game.init_game()
        stock_cards = state['game_state'].stock_cards
        self.assertEqual(len(stock_cards), 32)

    def test_get_player_id(self):
        game = KeezenGameAdapter()
        _, player_id = game.init_game()
        current = game.get_player_id()
        self.assertEqual(player_id, current)

    def test_get_legal_actions(self):
        game = KeezenGameAdapter()
        state, _ = game.init_game()
        legal_actions = state['legal_actions']
        for action in legal_actions:
            action_str = GameActions.ALL_ACTIONS_271[action]
            self.assertIn(action_str, game._ACTION_SPACE)

    def test_step(self):
        game = KeezenGameAdapter()
        state, _ = game.init_game()
        legal_actions = state['legal_actions']
        action = np.random.choice(list(legal_actions.keys()))
        action_str = GameActions.ALL_ACTIONS_271[action]
        state, next_player_id = game.step(action_str)
        self.assertEqual(state['game_state'].move_number, 1)

    def test_get_rewards(self):
        game = KeezenGameAdapter()
        state, _ = game.init_game()
        while not game.is_over():
            legal_actions = state['legal_actions']
            action = np.random.choice(list(legal_actions.keys()))
            action_str = GameActions.ALL_ACTIONS_271[action]
            state, next_player_id = game.step(action_str)
        _, rewards = game.game.is_over(game.game_state)
        self.assertEqual(sum(rewards), 2)


if __name__ == '__main__':
    unittest.main()
