import unittest
import numpy as np

import rlcard
from rlcard.agents.random_agent import RandomAgent
from rlcard.games.keezen.game import GameActions


class TestKeezenEnv(unittest.TestCase):

    def test_reset_and_extract_state(self):
        env = rlcard.make('keezen')
        state, _ = env.reset()
        self.assertEqual(state['obs'].size, 615)

    def test_get_legal_actions(self):
        env = rlcard.make('keezen')
        env.set_agents([RandomAgent(env.num_actions) for _ in range(env.num_players)])
        env.reset()
        legal_actions = env._get_legal_actions()
        for legal_action in legal_actions.keys():
            self.assertLessEqual(legal_action, 271)

    def test_step(self):
        env = rlcard.make('keezen')
        state, _ = env.reset()
        action = np.random.choice(list(state['legal_actions'].keys()))
        _, player_id = env.step(action)
        self.assertEqual(player_id, env.game.players.index(env.game.game_state.move_player))

    def test_run(self):
        env = rlcard.make('keezen')
        env.set_agents([RandomAgent(env.num_actions) for _ in range(env.num_players)])
        trajectories, rewards = env.run(is_training=False)
        self.assertEqual(len(trajectories), 4)
        self.assertEqual(sum(rewards), 2)
        trajectories, rewards = env.run(is_training=True)
        self.assertEqual(sum(rewards), 2)

    def test_decode_action(self):
        env = rlcard.make('keezen')
        env.reset()
        legal_actions = env._get_legal_actions()
        for legal_action in legal_actions:
            decoded = env._decode_action(legal_action)
            self.assertEqual(decoded, GameActions.ALL_ACTIONS_271[legal_action])


if __name__ == '__main__':
    unittest.main()
