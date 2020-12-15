from typing import Dict, Optional, Tuple
from . import Player, Utils
import os


class Matrix:
    __size: int
    __matrix: Dict[int, Dict[int, Optional[Player.Player]]]

    @staticmethod
    def parse_coord(coord: str) -> Optional[Tuple[int, int]]:
        """
        Parses a couple of coordinates and returns them as an integer number tuple.
        :param coord: The coordinates to parse.
        :type coord: str
        :return: A tuple containing the parsed coordinates
        """
        try:
            coord = coord.replace(' ', '')
            index: int = coord.find(',')
            x: int = int(coord[:index])
            if x < 0:
                return None
            y: int = int(coord[index + 1:])
            if y < 0:
                return None
            return x, y
        except ValueError:
            return None

    @staticmethod
    def setup_game_matrix():
        message: str = 'How big should the matrix be? '
        error_message: str = 'You must provide a valid matrix size!'
        size: int = Utils.Utils.prompt_number(message, error_message, False)
        return Matrix(size)

    def __build_matrix(self) -> None:
        """
        Generates the whole game matrix.
        """
        self.__matrix = {}
        # Generate a squared matrix according to the size defined.
        for row in range(self.__size):
            self.__matrix[row]: Dict[int, Player.Player] = {}
            for column in range(self.__size):
                self.__matrix[row][column] = None

    def __init__(self, size: int):
        """
        The class constructor.
        :param size: The game matrix size.
        :type size: int
        """
        self.__size = size
        # Generate the game matrix.
        self.__build_matrix()

    def get_size(self) -> int:
        """
        Returns the game matrix size.
        :return: The game matrix size.
        :rtype: int
        """
        return self.__size

    def get_cell(self, coords: Tuple[int, int]) -> Optional[Player.Player]:
        """
        Returns the player that has ticked the given cell.
        :return: The player that has ticked the given cell.
        :rtype: int
        """
        return self.__matrix[coords[0]][coords[1]]

    def draw(self) -> None:
        """
        Draws a graphical representation of the game matrix on the CLI.
        """
        # Print the matrix header.
        print('   +', end='')
        for row in range(self.__size):
            if row < 10:
                print(' 0' + str(row) + ' |', end='')
            else:
                print(' ' + str(row) + ' |', end='')
        print()
        # Print the matrix content.
        for row in range(self.__size):
            # Print the row number.
            if row < 10:
                print('0' + str(row) + ' |', end='')
            else:
                print(str(row) + ' |', end='')
            # Print the remaining columns.
            for column in range(self.__size):
                if self.__matrix[row][column] is None:
                    print('    |', end='')
                else:
                    print('\033[' + str(self.__matrix[row][column].get_color()) + 'm ██ \033[0m|', end='')
            print()

    def redraw(self) -> None:
        """
        Clears the screen and then print out the game matrix.
        :return:
        """
        # Clean up the screen.
        os.system('cls' if os.name == 'nt' else 'clear')
        # Draw the game matrix.
        self.draw()

    def is_cell_free(self, coords: Tuple[int, int]) -> bool:
        """
        Returns if a given cell is free.
        :param coords: The coordinates of the cell to be checked.
        :type coords: Tuple[int, int]
        :return: If the given cell is free will be returned true, false otherwise.
        :rtype: bool
        """
        return self.__matrix[coords[0]][coords[1]] is None

    def is_full(self) -> bool:
        """
        Returns if every matrix cell has been occupied or not.
        :return: If every matrix cell has been occupied will be returned true, false otherwise.
        :rtype: bool
        """
        full: bool = True
        # Iterate the game matrix in order to find a free cell.
        for row in range(self.__size):
            for column in range(self.__size):
                if self.__matrix[row][column] is None:
                    full = False
                    break
            if not full:
                break
        return full

    def tick_cell(self, player: Player.Player, coords: Tuple[int, int]) -> None:
        """
        Marks a given cell as occupied by a given player.
        :param player: The occupant player.
        :type player: Player.Player
        :param coords: The coordinates of the cell to be occupied.
        :type coords: Tuple[int, int]
        """
        # Mark the given cell if none has marked it yet.
        if self.is_cell_free(coords):
            self.__matrix[coords[0]][coords[1]] = player
