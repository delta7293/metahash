import metahash.config
import subprocess
import argparse
import bittensor as bt


def is_cuda_available():
    try:
        output = subprocess.check_output(["nvidia-smi", "-L"], stderr=subprocess.STDOUT)
        if "NVIDIA" in output.decode("utf-8"):
            return "cuda"
    except Exception:
        pass
    try:
        output = subprocess.check_output(["nvcc", "--version"]).decode("utf-8")
        if "release" in output:
            return "cuda"
    except Exception:
        pass
    return "cpu"


def add_args(parser):
    """
    Adds relevant arguments to the parser for operation.
    """

    parser.add_argument("--netuid", type=int, help="Subnet netuid", default=1)

    parser.add_argument(
        "--neuron.device",
        type=str,
        help="Device to run on.",
        default=is_cuda_available(),
    )

    parser.add_argument(
        "--neuron.epoch_length",
        type=int,
        help="The default epoch length (how often we set weights, measured in 12 second blocks).",
        default=360,
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Mock neuron and all network components.",
        default=False,
    )

    parser.add_argument(
        "--neuron.events_retention_size",
        type=str,
        help="Events retention size.",
        default=2 * 1024 * 1024 * 1024,  # 2 GB
    )

    parser.add_argument(
        "--neuron.dont_save_events",
        action="store_true",
        help="If set, we dont save events to a log file.",
        default=False,
    )

    parser.add_argument(
        "--wandb.off",
        action="store_true",
        help="Turn off wandb.",
        default=False,
    )

    parser.add_argument(
        "--wandb.offline",
        action="store_true",
        help="Runs wandb in offline mode.",
        default=False,
    )

    parser.add_argument(
        "--wandb.notes",
        type=str,
        help="Notes to add to the wandb run.",
        default="",
    )


def add_miner_args(parser):
    """Add miner specific arguments to the parser."""

    parser.add_argument(
        "--neuron.name",
        type=str,
        help="Trials for this neuron go in neuron.root / (wallet_cold - wallet_hot) / neuron.name. ",
        default="miner",
    )

    parser.add_argument(
        "--blacklist.force_validator_permit",
        action="store_true",
        help="If set, we will force incoming requests to have a permit.",
        default=True,
    )

    parser.add_argument(
        "--no-blacklist.force_validator_permit",
        action="store_false",
        dest="blacklist.force_validator_permit",
        help="If set, we will NOT force incoming requests to have a permit.",
    )

    parser.add_argument(
        "--blacklist.minimum_stake_requirement",
        type=int,
        help="Minimum amount of stake needed to send request to miners.",
        default=1_000,
    )

    parser.add_argument(
        "--blacklist.allow_non_registered",
        action="store_true",
        help="If set, miners will accept queries from non registered entities. (Dangerous!)",
        default=False,
    )

    parser.add_argument(
        "--wandb.project_name",
        type=str,
        default="template-miners",
        help="Wandb project to log to.",
    )

    parser.add_argument(
        "--wandb.entity",
        type=str,
        default="opentensor-dev",
        help="Wandb entity to log to.",
    )


def add_validator_args(parser):
    """Add validator specific arguments to the parser."""

    parser.add_argument(
        "--neuron.name",
        type=str,
        help="Trials for this neuron go in neuron.root / (wallet_cold - wallet_hot) / neuron.name. ",
        default="validator",
    )

    parser.add_argument(
        "--neuron.timeout",
        type=float,
        help="The timeout for each forward call in seconds.",
        default=10,
    )

    parser.add_argument(
        "--neuron.num_concurrent_forwards",
        type=int,
        help="The number of concurrent forwards running at any time.",
        default=1,
    )

    parser.add_argument(
        "--neuron.sample_size",
        type=int,
        help="The number of miners to query in a single step.",
        default=50,
    )

    parser.add_argument(
        "--neuron.axon_off",
        "--axon_off",
        action="store_true",
        # Note: the validator needs to serve an Axon with their IP or they may
        #   be blacklisted by the firewall of serving peers on the network.
        help="Set this flag to not attempt to serve an Axon.",
        default=False,
    )

    parser.add_argument(
        "--neuron.vpermit_tao_limit",
        type=int,
        help="The maximum number of TAO allowed to query a validator with a vpermit.",
        default=4096,
    )

    parser.add_argument(
        "--wandb.project_name",
        type=str,
        help="The name of the project where you are sending the new run.",
        default="template-validators",
    )

    parser.add_argument(
        "--wandb.entity",
        type=str,
        help="The name of the project where you are sending the new run.",
        default="opentensor-dev",
    )


def config():
    """
    Returns the configuration object specific to this miner or validator after adding relevant arguments.
    """
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    bt.wallet.add_args(parser)
    bt.subtensor.add_args(parser)
    bt.logging.add_args(parser)
    bt.axon.add_args(parser)
    add_validator_args(parser)
    add_miner_args(parser)
    add_args(parser)

    # Explicit config
    # Setting weights are disabled so we can trigger manually
    parser.add_argument(
        "--neuron.disable_set_weights",
        action="store_true",
        help="Disables setting weights.",
        default=True,
    )

    # For testing purposes
    parser.add_argument(
        "--no_epoch",
        action="store_true",      # becomes True if flag is present
        default=False,            # otherwise remains False
        help="Enable mock mode (no real chain calls).",
    )

    # 1.0 so it reset completely the scores
    parser.add_argument(
        "--neuron.moving_average_alpha",
        type=float,
        help="Moving average alpha parameter, how much to add of the new observation.",
        default=1,
    )

    parser.add_argument(
        "--neuron.axon_off",
        "--axon_off",
        action="store_true",
        # Note: the validator needs to serve an Axon with their IP or they may
        #   be blacklisted by the firewall of serving peers on the network.
        help="Set this flag to not attempt to serve an Axon.",
        default=True,
    )

    return bt.config(parser)
