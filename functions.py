import argparse
import configparser
import csv
import logging


def setup_logging(log_level):
    try:
        if log_level.isdigit():
            level = int(log_level)
        else:
            level = getattr(logging, log_level.upper())
    except AttributeError:
        level = logging.INFO

    logging.basicConfig(
        filename='chase.log',
        filemode='w',
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parser_func():
    parser = argparse.ArgumentParser(
        description="Simulation of sheep and wolf")

    parser.add_argument("-c", "--config", type=str, metavar='FILE',
                        help='Path to config file')

    parser.add_argument('-l', '--log', type=str, metavar='LEVEL',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL'],
                        help='Log level: DEBUG, INFO, WARNING, ERROR,'
                             'or CRITICAL')

    parser.add_argument("-r", "--rounds", type=int, default=50,
                        metavar='NUM',
                        help="The maximum number of rounds")

    parser.add_argument("-s", "--sheep", type=int, default=15,
                        metavar='NUM',
                        help="The number of sheep")

    parser.add_argument("-w", "--wait", action="store_true",
                        help="Pause simulation after each round until "
                             "key pressed")

    args = parser.parse_args()

    if args.rounds <= 0:
        raise ValueError(
            "The number of rounds must be an integer greater than zero")

    if args.sheep <= 0:
        raise ValueError(
            "The number of sheep must be an integer greater than zero")

    return args


def load_config(config_file):
    config = configparser.ConfigParser()
    read_files = config.read(config_file)

    if not read_files:
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}")

    try:
        sheep_init_pos = float(config["Sheep"]["InitPosLimit"])
        sheep_move_dist = float(config["Sheep"]["MoveDist"])
        wolf_move_dist = float(config["Wolf"]["MoveDist"])

    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")

    if sheep_init_pos <= 0:
        raise ValueError("InitPosLimit must be positive.")
    if sheep_move_dist <= 0:
        raise ValueError("Sheep MoveDist must be positive.")
    if wolf_move_dist <= 0:
        raise ValueError("Wolf MoveDist must be positive.")

    return sheep_init_pos, sheep_move_dist, wolf_move_dist


def count_alive_sheeps(sheeps):
    return len([sheep for sheep in sheeps if sheep.is_alive()])


def one_round(sheeps, wolfs):
    for sheep in sheeps:
        if sheep.alive:
            sheep.random_move(logging)
    logging.info("All alive sheep moved.")
    logging.info("All alive sheep moved.")
    closest_sheep = wolfs.find_closest_sheep(sheeps)
    seq = sheeps.index(closest_sheep) + 1
    dist = wolfs.euclidean_distance(closest_sheep)
    logging.debug(
        f"Wolf determined closest sheep {seq} at distance {dist}")
    logging.info(f"Wolf is chasing sheep {seq}")
    killed = wolfs.move(closest_sheep, sheeps)
    if killed:
        logging.info(f"Sheep {seq} was eaten.")
    logging.debug(f"Wolf moved to: {wolfs.get_position()}")
    logging.info("Wolf moved.")


def basic_information_print(sheeps, wolfs, round_number):
    # data
    x_wolf, y_wolf = wolfs.get_position()
    alive_sheeps = count_alive_sheeps(sheeps)
    # printing
    print(f"Round number: {round_number}")
    print(f"Wolf position: ({x_wolf:.3f}, {y_wolf:.3f})")
    print(f"The number of sheeps alive: {alive_sheeps}")
    print("-" * 20)


def json_file_data(sheeps, round_number, simulation_data, wolfs):
    x_wolf, y_wolf = wolfs.get_position()
    sheep_positions = []

    for sheep in sheeps:
        if sheep.alive:
            x_sheep, y_sheep = sheep.get_position()
            sheep_positions.append(
                (round(x_sheep, 3), round(y_sheep, 3)))
        else:
            sheep_positions.append(None)
    round_dict = {
        "round_no": round_number,
        "wolf_pos": (round(x_wolf, 3), round(y_wolf, 3)),
        "sheep_pos": sheep_positions
    }

    simulation_data.append(round_dict)
    return simulation_data


def csv_file_data(sheeps, round_number):
    alive_count = count_alive_sheeps(sheeps)

    with open('alive.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([round_number, alive_count])
    logging.debug("Information saved to alive.csv")
