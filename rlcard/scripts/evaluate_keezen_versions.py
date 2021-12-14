""" Tournament between two versions of trained models
Evaluate trained models by autoplay tournament against each other."""
import os
import argparse
import rlcard
from rlcard.utils import get_device, set_seed, tournament


def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
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
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, args.num_games)
    for position, reward in enumerate(rewards):
        print(position, args.models[position], reward)
    return rewards


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument('--env', type=str, default='keezen',
            choices=['blackjack', 'leduc-holdem', 'limit-holdem', 'doudizhu', 'mahjong', 'no-limit-holdem', 'uno', 'gin-rummy', 'keezen'])
    parser.add_argument('--cuda', type=str, default='')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--num_games', type=int, default=2000)
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # Get all model file names, get the number of frames and order descending
    path = './experiments/dmc_keezen_result/keezenexpid7/'
    frames1 = '1000435200'
    frames2 = '2002457600'

    # Tournament:
    # Random
    # 1000435200
    # 2002457600
    # 3002022400
    # 4096486400
    # 7016000000
    # 10512601600

    arg0 = path + "0_" + frames1 + ".pth"
    arg1 = path + "1_" + frames2 + ".pth"
    arg2 = path + "2_" + frames1 + ".pth"
    arg3 = path + "3_" + frames2 + ".pth"
    parser.add_argument('--models', nargs='*', default=[arg0, arg1, arg2, arg3])
    args = parser.parse_args()

    print('Tournament: ' + str(args.num_games) + 'x ' + frames1 + "-" + frames2)
    rewards = evaluate(args)

