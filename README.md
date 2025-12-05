# Wolf and Sheep Simulation

A turn-based simulation of a predator-prey relationship in an infinite 2D meadow, developed in Python.

## Project Description

This project simulates a chase between a single wolf and a herd of sheep on an infinite Cartesian plane.
* **The Wolf** starts at coordinates `(0.0, 0.0)`. It tracks the nearest sheep and attempts to catch it.
* **The Sheep** start at random positions. They move clumsily in random cardinal directions (N, S, E, W) to escape.

The simulation runs in rounds. In each round, all sheep move first, followed by the wolf. If the wolf gets close enough to a sheep (within its attack range), the sheep is eaten.

## Project Structure

The project is modularized into the following files:

* **`main.py`**: The entry point of the application. Manages the simulation loop, initializes agents, and handles data saving.
* **`wolfAgent.py`**: Contains the `WolfAgent` class with logic for tracking and chasing sheep using Euclidean distance math.
* **`sheepAgent.py`**: Contains the `SheepAgent` class with logic for random movement and boundary checks.
* **`functions.py`**: Helper functions for argument parsing, configuration loading, logging setup, and file operations (`json`/`csv`).

## Usage

### Basic Run
Run the simulation with default parameters (15 sheep, 50 rounds):
```bash
python main.py

python main.py [-h] [-c FILE] [-l LEVEL] [-r NUM] [-s NUM] [-w]
```
Argument,Description
* "-h, --help",Show this help message and exit.
* "-c, --config",Path to an external configuration file (INI format).
* "-l, --log","Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Logs are saved to chase.log."
* "-r, --rounds",Maximum number of rounds (default: 50).
* "-s, --sheep",Number of sheep (default: 15).
* "-w, --wait",Pause simulation after each round (press Enter to continue).

### Output Files

The simulation generates three files in the working directory:
* **pos.json**: A JSON dump of all animal positions per round.
Format: List of dictionaries containing round_no, wolf_pos, and sheep_pos.
Note: Dead sheep are represented as null.
* **alive.csv**: A CSV file tracking survival statistics.
Format: Round Number, Alive Sheep Count.
* **chase.log**: A log file containing simulation events based on the selected log level.

## Requirements

* Python 3.6+
* Standard libraries used: `random`, `math`, `json`, `csv`, `argparse`, `configparser`, `logging`.
