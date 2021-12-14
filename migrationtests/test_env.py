import unittest

from agent import RandomAgent, RuleBasedAgent
from env import Env


class TestEnv(unittest.TestCase):

    def setUp(self) -> None:
        self.env = Env()
        self.game_state = self.env.reset()

        self.agents = [RuleBasedAgent(self.env.game), RandomAgent(self.env.game), RuleBasedAgent(self.env.game),
                       RandomAgent(self.env.game)]

    # def test_random_agent(self):
    #     move = agent.get_move(None, None)
    #     self.assertEqual(None, move)
    #     move1 = Move(MoveType.START, Player("test", FieldColor.RED, PlayerLocation.EAST), [Card(Suit.CLUBS,
    #                                                                                        CardValue.ACE, "1")], [])
    #     move = agent.get_move([move1], None)
    #     self.assertEqual(move1, move)
    #
    # def test_rule_based_agent(self):
    #     agent = RuleBasedAgent(self.game)
    #     move = agent.get_move(None, None)
    #     self.assertEqual(None, move)
    #     move1 = Move(MoveType.START, Player("test", FieldColor.RED, PlayerLocation.EAST), [Card(Suit.CLUBS,
    #                                                                                        CardValue.ACE, "1")], [])
    #     move = agent.get_move([move1], None)
    #     self.assertEqual(move1, move)


if __name__ == '__main__':
    unittest.main()
