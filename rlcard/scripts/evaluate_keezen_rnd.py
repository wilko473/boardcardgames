""" Runs a tournament of two trained DMC models against two randomly playing agents.
This script picks the newest not already processed model from the experiment id path.
Already processed models and the results are in the file processed.csv.
Typically, this script is run from a cron job.
The script create_graph_rnd.py renders a graph from the file processed.csv.
Set the path of the experiment.
"""
import csv
import fnmatch
import os
import argparse
import rlcard
from rlcard.utils import get_device, set_seed, tournament
from collections import OrderedDict


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
    parser.add_argument('--cuda', type=str, default='0')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--num_games', type=int, default=1000)

    # Get all model file names, get the number of frames and order descending
    path = './experiments/dmc_keezen_result/keezenexpid8/'
    files = fnmatch.filter(os.listdir(path), "*.pth")
    files = [file[:-4] for file in files]
    files = [file[2:] for file in files]
    files = list(dict.fromkeys(files))
    files.sort(key=int, reverse=True)
    print("Files: " + str(len(files)))

    if files:
        processed = OrderedDict()
        try:
            with open(path + 'processed.csv', 'r') as csv_file:
                reader = csv.reader(csv_file)
                processed = OrderedDict(reader)
            print("Already processed:" + str(len(processed)))
        except IOError:
            print("File does not exist, will be created")

        newest = None
        i = 0
        while i < len(files) and not newest:
            if files[i] not in processed.keys():
                newest = files[i]
            i = i + 1
        print("Newest:" + newest)
        if newest:
            arg0 = path + "0_" + newest + ".pth"
            arg2 = path + "2_" + newest + ".pth"
            parser.add_argument('--models', nargs='*', default=[arg0, 'random', arg2, 'random'])
            args = parser.parse_args()

            rewards = evaluate(args)

            processed[newest] = rewards[0]
            with open(path + 'processed.csv', 'w+') as csv_file:  # Truncate file
                writer = csv.writer(csv_file)
                for key, value in processed.items():
                    writer.writerow([key, value])

