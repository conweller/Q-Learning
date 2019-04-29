# Q-Learning Algorithm
This program uses a q-learning to solve to determine the best path to a goal
state.

Please run with python3 (version > 3.7)

## Usage
This program is run by calling:
```
python3 hw3.py <input>
```
To run main.py, input a command line argument in the format # # # X (#), where the
first three numbers indicate the index of the goal, forbidden, and wall squares
respectively on the board, and the fourth and fifth items specify the output. If
the character 'p' is given as the fourth argument, no fifth argument should be
given, and the program will print the optimal policies for each block on the
board. If the character 'q' is given, as the fourth argument, it will print the
'q' values found for each action taken from the index specified by the fifth
argument.
