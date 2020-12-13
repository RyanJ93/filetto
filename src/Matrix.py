from typing import Dict, Optional, Tuple
from . import Player
import os


class Matrix:
    __size: int
    __matrix: Dict[int, Dict[int, Optional[Player.Player]]]

    @staticmethod
    def parse_coord(coord: str) -> Optional[Tuple[int, int]]:
        try:
            coord = coord.replace(' ', '')
            index: int = coord.find(',')
            x: int = int(coord[:index])
            y: int = int(coord[index + 1:])
            return x, y
        except ValueError:
            return None

    def __build_matrix(self) -> None:
        self.__matrix = {}
        for row in range(self.__size):
            self.__matrix[row]: Dict[int, Player.Player] = {}
            for column in range(self.__size):
                self.__matrix[row][column] = None

    def __init__(self, size: int):
        self.__size = size
        self.__build_matrix()

    def get_size(self) -> int:
        return self.__size

    def get_column(self, coords: Tuple[int, int]) -> Optional[Player.Player]:
        return self.__matrix[coords[0]][coords[1]]

    def draw(self) -> None:
        print('   +', end='')
        for row in range(self.__size):
            if row < 10:
                print(' 0' + str(row) + ' |', end='')
            else:
                print(' ' + str(row) + ' |', end='')
        print()
        for row in range(self.__size):
            if row < 10:
                print('0' + str(row) + ' |', end='')
            else:
                print(str(row) + ' |', end='')
            for column in range(self.__size):
                if self.__matrix[row][column] is None:
                    print('    |', end='')
                else:
                    print('\033[' + str(self.__matrix[row][column].get_color()) + 'm ██ \033[0m|', end='')
            print()

    def redraw(self) -> None:
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[0;0H", end="")
        self.draw()

    def is_cell_free(self, coords: Tuple[int, int]) -> bool:
        return self.__matrix[coords[0]][coords[1]] is None

    def is_full(self) -> bool:
        full: bool = True
        for row in range(self.__size):
            for column in range(self.__size):
                if self.__matrix[row][column] is None:
                    full = False
                    break
            if not full:
                break
        return full

    def tick_cell(self, player: Player.Player, coords: Tuple[int, int]) -> None:
        if self.is_cell_free(coords):
            self.__matrix[coords[0]][coords[1]] = player
