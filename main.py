from typing import List, Tuple, Optional
from src import Player, Matrix

print('Welcome to filetto!')
players: Optional[List[Player.Player]] = None
# Setup players.
while players is None or len(players) < 2:
    if players is not None:
        print('There must be at least 2 players!')
    players = []
    Player.Player.setup_human_players(players)
    Player.Player.setup_ai_players(players)
if len(players) > 10:
    print('I cannot handle more than 10 players at once, exiting...')
    exit(0)
# Setup the game matrix.
matrix: Matrix = Matrix.Matrix.setup_game_matrix()
matrix.draw()
# Start the game loop
winner: Optional[Player.Player] = None
while not winner:
    full: bool = False
    # Ask to players to tick a cell.
    for player in players:
        # Stop looping is every cell has been ticked.
        full = matrix.is_full()
        if full:
            break
        if player.get_is_human():
            # Current player is a human player, he must provide coordinates.
            print(player.get_name() + ', where do you want to place a tick?')
            coords: Optional[Tuple[int, int]] = None
            while coords is None:
                # Parse the user provided coordinates.
                coords = Matrix.Matrix.parse_coord(input())
                if coords is None:
                    print('Please provide some valid coordinates!')
                else:
                    try:
                        if not matrix.is_cell_free(coords):
                            print('Please provide some valid coordinates!')
                            coords = None
                    except KeyError:
                        print('Please provide some valid coordinates!')
                        coords = None
            matrix.tick_cell(player, coords)
        else:
            # Current player is an AI player, generate the coordinates.
            coords: Optional[Tuple[int, int]] = Player.Player.pick_cord(matrix)
            matrix.tick_cell(player, coords)
        # Compute the player score and check if he has won the game.
        score: int = player.compute_score(matrix)
        if score >= 50:
            winner = player
    # Draw the whole matrix.
    matrix.redraw()
    # Draw the whole scoreboard.
    print('\nScoreboard:')
    for player in players:
        print(player.get_marker() + ' ' + player.get_name() + ': ' + str(player.get_score()))
    if winner:
        # We have a winner, announce him.
        print(winner.get_name() + ' won!!!')
    if not winner and full:
        # The whole board is full, the game has finished without a winner.
        print('Game over!')
