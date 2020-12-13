from typing import List, Tuple, Optional
from src import Player, Matrix

print('Welcome to filetto, how many human players are there? ', end='')
player_count: int = int(input())
current_index: int = 1
players: List[Player.Player] = []
for player_number in range(player_count):
    player_name: str = 'Player ' + str(current_index)
    player: Player = Player.Player(player_name, Player.Player.get_color_number(current_index), True)
    players.append(player)
    current_index += 1
print('How many AI players do you want to play with you? ', end='')
player_count = int(input())
for player_number in range(player_count):
    player_name: str = 'Player ' + str(current_index) + ' (AI)'
    player: Player = Player.Player(player_name, Player.Player.get_color_number(current_index), False)
    players.append(player)
    current_index += 1
print('How big should the matrix be? ', end='')
size: int = int(input())
matrix: Matrix = Matrix.Matrix(size)
matrix.draw()

winner: Optional[Player.Player] = None
while not winner:
    full: bool = False
    for player in players:
        full = matrix.is_full()
        if full:
            break
        if player.get_is_human():
            print(player.get_name() + ', where do you want to place a tick?')
            coords: Optional[Tuple[int, int]] = None
            while coords is None:
                coords = Matrix.Matrix.parse_coord(input())
                if coords is None:
                    print('Please provide some valid coordinates!')
                else:
                    if not matrix.is_cell_free(coords):
                        print('Please provide some valid coordinates2!')
                        coords = None
            matrix.tick_cell(player, coords)
        else:
            coords: Optional[Tuple[int, int]] = Player.Player.pick_cord(matrix)
            matrix.tick_cell(player, coords)
        score: int = player.compute_score(matrix)
        if score >= 50:
            winner = player
    matrix.redraw()
    print('\nScoreboard:')
    for player in players:
        print(player.get_marker() + ' ' + player.get_name() + ': ' + str(player.get_score()))
    if winner:
        print(winner.get_name() + ' won!!!')
    if not winner and full:
        print('Game over!')
