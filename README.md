# cse423 group project
# Treasure Hunter

## General Idea
The **treasure hunter (player)** searches for treasure underground in a forest full of unexpected surprises.

## Features
- Player moves forward, and backward, rotate clockwise,antoclockwise with **W, D, A, S** keys.
- Camera angle changes with **arrow keys**.
- Player mines the ground beneath their position using **mouse left click** (10 chances per round; resets on treasure found).
- Finding a treasure increases the score, and resets mining chances to 0.
- Finding a **fruit**: Player head turns green for 0.5 sec, speed increases (up to limit), and health bar increases by 1 (max 5, initialized initially).
- Finding a **wild mushroom**: Player turns red for 0.5 sec, loses 1 health bar, and speed decreases.

### Obstacles
- **Boulders and bushes**: Cannot mine under them.
- **bear**:
  - Attack player after 3 sec in their line of sight.
  - Destroy bushes/stones with **X** key press.
  - Monkey attacks: Lose 2 treasures. Avoid by moving or hiding.
  - Tiger attacks: Lose 3 health bars. Avoid by moving or hiding.

### Cheat Modes
- Become invisible for 3/5 sec (monkeys and tigers ignore player).
- Scan area to reveal all underground treasures for 1 sec.

## Game End Conditions
- Three wild mushrooms in a row.
- Three monkey attacks in a row.
- Two tiger attacks in a row.
- Health bar reaches 0.
- **Win:** Score reaches 10.
- **Fail:** No treasure found in 10 attempts.


# by 22301690 - Sajid Bin Kawsar
23101341 - SHAFEEN IBNEY FAROOK
22201753 - Aurpon Sharma
