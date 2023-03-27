# Distributed Tic-Tac-Toe
Project for Distributed Systems course 

Glib Manaiev, Dmytro Fedorenko, Ekaterina Sedykh

This project implements a distributed tic-tac-toe game following a leader/coordinator architecture, consisting of 3 Nodes (computers). Nodes are interconnected via gRPC and implement the same functionality. The game can be played by two players, each assigned with a particular symbol (O or X).

## Available Commands
-**Start-game**: Set up the game environment, synchronize Node clocks, and elect a leader (game master) to provide the board, assign symbols, and regulate turns.

-**Set-symbol**: Used by a player during their turn to place their assigned symbol (O or X) on the board.

-**List-board**: Display the current state of the board for any player or the game master, including placed symbols and timestamps.

-**Set-node-time Node-N <hh:mm:ss>**: Modify the internal clock of a specific Node, with the leader having authority to modify any clock in the system, while workers can only modify their internal clock.

-**Set-time-out**: The leader tracks and enforces time-outs in the system, with default settings and options for players to reset the game under certain conditions.

The leader monitors the game and decides the winner. Once a player wins the game, the leader notifies all players of the outcome and resets the system for a new game.
