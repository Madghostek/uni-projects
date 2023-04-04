# two-player-games
Library of two-player logical games for WUT students

## Architecture

Two primary base classes of the games are `Game` and `State`.

These two classes have very similar functionalities, with the following differences:
 - a `Game` object contains a `State` object
 - making move on a `Game` object changes its state while making move on a `State` object returns new state without affecting the previous one.
 - a `State` object may have more game-specific functionalities

Common functionalities of `Game` and `State`:
 - getting the list of avaliable moves
 - getting current player
 - checking if a game has finished
