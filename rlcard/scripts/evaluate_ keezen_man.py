""" Manual analyzer
Observe a game of four trained models.
Hit enter to step through the game.
Set path of the experiment and identify the agent by the number of frames.
"""
import os
import argparse
import torch
import rlcard
from rlcard.utils import set_seed
from rlcard.games.keezen.game import GameActions


def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    else:
        from rlcard import models
        agent = models.load(model_path).agents[position]

    return agent


def evaluate(args):
    """Manually evaluate a game of 4 DMC trained agents."""
    device = torch.device("cpu")
    set_seed(args.seed)
    env = rlcard.make(args.env, config={'seed': args.seed})
    agents = []
    for position, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)
    state, player_id = env.reset()

    while not env.is_over():
        # Agent plays
        action = env.agents[player_id].step(state)

        # Environment steps
        next_state, next_player_id = env.step(action, env.agents[player_id].use_raw)

        # Set the state and player
        state = next_state
        player_id = next_player_id

        env.game.render()
        print("Last action: " + str(GameActions.ALL_ACTIONS_271[action]))

        input("Enter for next move")
    payoffs = env.get_payoffs()
    print("Finished: payoffs = " + str(payoffs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Manual evaluation in RLCard")
    parser.add_argument('--env', type=str, default='keezen',
                        choices=['blackjack', 'leduc-holdem', 'limit-holdem', 'doudizhu', 'mahjong', 'no-limit-holdem',
                                 'uno', 'gin-rummy', 'keezen'])
    parser.add_argument('--cuda', type=str, default='0')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--num_games', type=int, default=1000)

    path = './experiments/dmc_keezen_result/keezenexpid8/'
    frames = '10512601600'  # Number of trained frames. Selects the agent to observe.
    arg0 = path + "0_" + frames + ".pth"
    arg1 = path + "1_" + frames + ".pth"
    arg2 = path + "2_" + frames + ".pth"
    arg3 = path + "3_" + frames + ".pth"
    parser.add_argument('--models', nargs='*', default=[arg0, arg1, arg2, arg3])
    args = parser.parse_args()

    evaluate(args)


