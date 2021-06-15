# Kuba
A python implementation of the board-game, Kuba.

## Objective
A player wins by pushing off and capturing seven neutral red stones or by pushing off all of the opposing stones.  A player who has no legal moves available has lost the game.

## Game Rules
With alternating turns, players move a single marble in any orthogonal direction.  In order to slide a marble, however, there must be access to it.  For example, to slide a marble to the left, the cell just to the right if it must be vacant.  If there are other marbles; your own, your opponent's or the neutral red ones; in the direction of your move at the cell you are moving to, those marbles are pushed one cell forward along the axis of your move.  Up to six marbles can be pushed by your one marble on your turn.  Although a player cannot push off one of his own marbles, any opposing counters that are pushed off are removed from the game and any neutral counters that are pushed off are captured by the pushing player to add to his or her store of captured neutral red marbles.  If you manage to push off a neutral or opposing marble, you are entitled to another turn.

## How to play:
