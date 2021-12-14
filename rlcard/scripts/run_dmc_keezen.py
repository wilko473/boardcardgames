"""Train DMC on Keezen.
Outputs the models to experiments/experimentid directory.
"""
import argparse
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer


def train(args):
    env = rlcard.make(args.env)

    trainer = DMCTrainer(env,
                         load_model=args.load_model,
                         xpid=args.xpid,
                         savedir=args.savedir,
                         save_interval=args.save_interval,
                         num_actor_devices=args.num_actor_devices,
                         num_actors=args.num_actors,
                         training_device=args.training_device,
                         num_buffers=32)
    trainer.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("DMC Keezen in RLCard")
    parser.add_argument('--env', type=str, default='keezen',
                        choices=['blackjack', 'leduc-holdem', 'limit-holdem', 'doudizhu', 'mahjong', 'no-limit-holdem',
                                 'uno', 'gin-rummy', 'keezen'])
    parser.add_argument('--cuda', type=str, default='0')
    parser.add_argument('--load_model', action='store_true', default=True,
                        help='Load an existing model')
    parser.add_argument('--xpid', default='keezenexpid8',
                        help='Experiment id (default: keezenexpid8)')
    parser.add_argument('--savedir', default='experiments/dmc_keezen_result',
                        help='Root dir where experiment data will be saved')
    parser.add_argument('--save_interval', default=120, type=int,
                        help='Time interval (in minutes) at which to save the model')
    parser.add_argument('--num_actor_devices', default=1, type=int,
                        help='The number of devices used for simulation')
    parser.add_argument('--num_actors', default=5, type=int,
                        help='The number of actors for each simulation device')
    parser.add_argument('--training_device', default=0, type=int,
                        help='The index of the GPU used for training models')
    args = parser.parse_args()

    train(args)
