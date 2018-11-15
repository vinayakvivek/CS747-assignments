## SARSA agent in the Windy GridWorld
Objective of this assignment is to test a SARSA reinforcement learning agent in the Windy GridWorld (Example 6.5, Sutton and Barto)

### files
- `windy_grid.py`
    - contains the class `WindyGrid` which simulates the environment.
    - `WindyGrid.step()` function returns `(next_state, reward, done)` given action.
    - it keeps track of current position/state.
- `sarsa.py`
    - contains the class `SarsaAgent` which implements the sarsa algorithm.
    - takes in following command line arguments
        ```bash
        --env E       path to environment description file
        --logdir L    log directory
        --alpha 𝛼     learning rate (default: 0.5)
        --gamma 𝛾     discount factor (default: 1)
        --epsilon 𝜀   exploration rate (default: 0.01)
        --seed r      random seed (default: 1)
        --episodes N  number of episodes to run (default: 200)
        ```
- `envs/*`: environment description files (explained in next section)
- `logs/*`: experiment log files. csv files with each row as <episode, steps, cumulative_steps>
- `plots/*`: experiment plots

### Environment description file
- JSON file. Checkout this sample.
    ```json
    {
        "size": [10, 7],
        "start": [0, 3],
        "goal": [7, 3],
        "wind": [0, 0, 0, 1, 1, 1, 2, 2, 1, 0],
        "king_move": false,
        "stochastic": false
    }
    ```

### Running experiments
- `run.sh` takes in six arguments.
    ```bash
    ./run.sh <env_path> <log_dir> <alpha> <epsilon> <num_episodes> <num_runs>
    ```
    - `env_path`: path to environment description file
    - `log_dir`: directory to which log files should be written
    - `num_runs`: runs with separate random seeds
- example usage:
    ```bash
    ./run.sh envs/env0.json logs/env0 0.5 0.01 200 10
    ```
- after running this command, log can be found in specified `log_dir` and corresponding plot in `plots/`
- use this script to run experiment each of the four environments.
    ```bash
    ./run.sh envs/env0.json logs/env0 0.5 0.01 200 10
    ./run.sh envs/env1.json logs/env1 0.5 0.01 200 10
    ./run.sh envs/env2.json logs/env2 0.5 0.01 200 10
    ./run.sh envs/env3.json logs/env3 0.5 0.01 200 10
    ```
