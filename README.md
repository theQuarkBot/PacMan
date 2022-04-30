# PacMan

https://github.com/theQuarkBot/PacMan

Overview of Code:

Bin: Contains images that were used to represent the ghosts and pacman, 
Also contains fonts used for our screens.

board.py: Contains the Board class. When called, creates a pygame screen with 
our board/map on it.

main.py: Is the center that links all other files together. Creates all objects
that are needed for the game and has the while loop that runs until the game is
over.

pacman_class.py: Contains the Pacman, Ghost, and RandomGhost classes. All 
functionalities of each object are declared here with all movement and 
collision parameters(with walls) are here.

screens.py: Contains buttons for the start screen, the start screen and the 
gameover screen. Used by main.py for us to know which version of the game the 
user wants to play.

settings.py: Contains constant values that every other class uses, such as game
states, pygame controls, starting locations of pacman and ghosts, etc.

thread_safe_classes.py: Contains two classes that are used by the Pacman, Ghost
and RandomGhost classes in order for us to thread the objects safely without 
race conditions or deadlocks.

Instructions on how to run:
1. Have all files and bin in one folder
2. Make sure you are able to run pygame on your device
3. Call python3 main.py
4. Pick if 1 player or 2 player mode wants to play, if 2 find a friend.
5. Pacman moves with arrow keys and Ghost moves with WASD
6. Play the game!
