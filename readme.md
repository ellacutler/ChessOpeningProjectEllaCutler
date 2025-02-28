## Introduction 
I want to make a tool for my friend who wants to study chess openings.

Functionally, this is akin to creating a flashcard management tool, where the individual cards are chess contexts/sequences. 

My friend gave me a file with openings he would want to use as "flashcards"  and now my job is to do the following:

1) Create interface that includes a screen, chess board, ways to manage user state, and ways to manage "opening state" 

2) Eventually, to add the spaced repetition algorithm so "opening cards" are only reviewed when completely necessary, to reduce the practice load on my friend. 


## High Level Code-Organization

At its core, this project will be comprised of different *components* that are in service of achieving this goal.



*  `board.py`, which manages the board state, including where pieces are and what moves are legal. This inherits from the `chess.board` module and may also have additional methods as the need arises.

* `game.py` which routes user click input to a relevant other component, like to check if a user is attempting to make a chess move. This is more or less an event handler that ties the other components together. 

* `screen.py` handles most of the non-event management from `pygame` and all rendering, including rendering of pieces

* `opening.py` defines the `Opening` and `OpeningSet` classes, which refer to the following:

    * `Opening` -> the *sequence of moves* in any given opening. This implements relevant `sequence` methods including `__next__` and `__iter__`.  
    
    * `OpeningList` -> a list of `Openings` that the tool then presents to the user/my friend, which will also eventually implement `sequence` methods including `__next__` and `__iter__`. Eventually, `OpeningList` will include filtering functionalities to only present the needed cards in any given practice session.

* `move.py` , which interfaces in between `game.py` and `board.py` to translate between screen state and board state. 

* `run.py` which manages the actual python executable that runs the game. 

## Where I am Currently:

- Implemented core functionality in `board.py`, `game.py` , `screen.py` and `run.py`, so a student can as of right now play a chess game. I also have implemented some basic functionality in `opening.py` and have lightly integrated it into the system. Also added buttons for features that my friend would like to have in the future. 

- My next steps is to first to fully flesh out `opening.py`, so the flashcard functionality works. After that point, I will then implement the spaced repetition system.


## Resources 

* [Spaced Repetition](https://www.justinmath.com/cognitive-science-of-learning-spaced-repetition/)
