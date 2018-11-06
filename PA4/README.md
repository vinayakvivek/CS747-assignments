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
        --alpha 𝛼     learning rate (default: 0.5)
        --gamma 𝛾     discount factor (default: 1)
        --epsilon 𝜀   exploration rate (default: 0.01)
        --episodes N  number of episodes to run (default: 200)
        --plot        to plot the graph.
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
- usage:
    ```
    python3 sarsa.py [-h] --env E [--alpha 𝛼] [--gamma 𝛾] [--epsilon 𝜀]
                [--episodes N] [--plot]
    ```
- example usage:
    ```bash
    python3 sarsa.py --env envs/env0.json --alpha 0.5 --gamma 1 --epsilon 0.01 --episodes 20 --plot
    ```
