import json
import logging

import functions
import sheepAgent
import wolfAgent


def main():
    args = functions.parser_func()
    sheep_init_pos, sheep_move_dist, wolf_move_dist = (
        functions.load_config(args.config))
    functions.setup_logging(args.log)
    logging.debug(
        f"Configuration values loaded: InitPosLimit={sheep_init_pos}, "
        f"Sheep MoveDist={sheep_move_dist}, Wolf MoveDist="
        f"{wolf_move_dist}")

    # creates sheeps and wolf
    simulation_data = []
    sheeps = []
    wolf = wolfAgent.WolfAgent(wolf_move_dist)
    number_of_sheeps = args.sheep
    for i in range(number_of_sheeps):
        sheeps.append(sheepAgent.SheepAgent(i, sheep_init_pos,
                                            sheep_move_dist))
        logging.debug(
            f"Initial position of sheep {sheeps[i].id}:"
            f" {sheeps[i].get_position()}")
    logging.info("Initial positions of all sheep determined.")

    # makes rounds until one of the wolf eats all sheeps or 50 rounds
    functions.basic_information_print(sheeps, wolf, 0)
    for i in range(1, args.rounds + 1):
        logging.info(f"New round started: {i}")
        # round logic
        functions.one_round(sheeps, wolf)

        # everything about basic information files
        functions.basic_information_print(sheeps, wolf, i)
        simulation_data = functions.json_file_data(sheeps, i,
                                                   simulation_data,
                                                   wolf)
        functions.csv_file_data(sheeps, i)
        logging.info(
            f"Round about to end, number of alive sheep: "
            f"{functions.count_alive_sheeps(sheeps)}")
        if all(not sheep.alive for sheep in sheeps):
            logging.info(
                "Simulation terminated because all sheep are dead")
            break
        if args.wait:
            input("Press key to continue...")
    with open("pos.json", "w") as f:
        json.dump(simulation_data, f, indent=2)
    logging.debug("Information saved to pos.json")


if __name__ == "__main__":
    main()
