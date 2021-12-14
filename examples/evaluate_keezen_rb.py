"""Tournament of trained models against rule-based agents
Evaluates trained models by an autoplay tournament against two rule-based agents.
Set path of the experiment and identify the agent by the number of frames.
"""
import os
import argparse
import rlcard
from rlcard.games.keezen.agent import RuleBasedAgent, RuleBasedAgentAdapter
from rlcard.utils import get_device, set_seed, tournament


def load_model(model_path, env=None, position=None, device=None, game=None):
    if os.path.isfile(model_path):  # Torch model
        print("Torch: " + model_path)
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        print("Random")
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    elif model_path == 'rulebased':
        print("Rulebased")
        rb_agent = RuleBasedAgent(game)
        agent = RuleBasedAgentAdapter(rb_agent)
    return agent


def evaluate(args):

    # To use the cpu, if a training is claiming the GPU: device = torch.device("cpu")
    device = get_device()

    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make(args.env, config={'seed': args.seed})

    # Load models
    agents = []
    for position, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, position, device, env.game.game))
    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, args.num_games)
    for position, reward in enumerate(rewards):
        print(position, args.models[position], reward)
    return rewards


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument('--env', type=str, default='keezen',
                        choices=['blackjack', 'leduc-holdem', 'limit-holdem', 'doudizhu', 'mahjong', 'no-limit-holdem',
                                 'uno', 'gin-rummy', 'keezen'])
    parser.add_argument('--cuda', type=str, default='0')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--num_games', type=int, default=4000)

    path = './experiments/dmc_keezen_result/keezenexpid8/'
    frames = '4512537600'  # The number of frames of the model

    arg0 = path + "0_" + frames + ".pth"
    arg1 = "rulebased"
    arg2 = path + "2_" + frames + ".pth"
    arg3 = "rulebased"
    parser.add_argument('--models', nargs='*', default=[arg0, arg1, arg2, arg3])
    args = parser.parse_args()

    print('Tournament: ' + str(args.num_games) + 'x ' + frames + "-" + arg1)
    rewards = evaluate(args)

