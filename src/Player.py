from typing import List, Optional, Tuple, Dict
from random import randrange
from . import Utils


class Player:
    __name: str
    __color: int
    __is_human: bool
    __score: int

    @staticmethod
    def get_color_number(index: int) -> Optional[int]:
        """
        Returns a color number based on a given number from 0 to 9.
        :param index: The number that will be used to pick the output color.
        :type index: int
        :return: The chosen color as ANSI code or None if the given index number is not valid.
        :rtype: Optional[int]
        """
        colors: List[int] = [31, 32, 33, 34, 35, 36, 90, 91, 92, 96]
        if index < len(colors):
            return colors[index]
        else:
            return None

    @staticmethod
    def pick_cord(matrix) -> Optional[Tuple[int, int]]:
        """
        Returns a free cell that can be occupied by an AI player.
        :param matrix: The game matrix being used.
        :type matrix: Matrix.Matrix
        :return: The selected cell coordinates or none if the whole game matrix has been occupied.
        :rtype: Optional[Tuple[int, int]]
        """
        coords: Optional[Tuple[int, int]] = None
        # Check if at least one cell is available.
        if not matrix.is_full():
            size: int = matrix.get_size()
            # Iterate until a free cell is found.
            while coords is None:
                # Pick some random coordinates.
                coords = (randrange(size), randrange(size))
                # Check if the cell selected has already been occupied.
                value: Optional[Player] = matrix.get_cell((coords[0], coords[1]))
                if value is not None:
                    coords = None
        return coords

    @staticmethod
    def setup_human_players(players: List):
        """
        Asks the user to provide the human players amount and then initializes those players.
        :param players: The list the players should be added to.
        :type players: List[Player.Player]
        """
        message: str = 'How many human players are there? '
        error_message: str = 'You must provide a valid players amount!'
        player_count: int = Utils.Utils.prompt_number(message, error_message)
        # Get next index in order to assign a color to the player.
        current_index: int = len(players) + 1
        for player_number in range(player_count):
            # Generate a name for the player and then initialize it.
            player_name: str = 'Player ' + str(current_index)
            player: Player = Player(player_name, Player.get_color_number(current_index), True)
            players.append(player)
            current_index += 1

    @staticmethod
    def setup_ai_players(players: List) -> None:
        """
        Asks the user to provide the AI players amount and then initializes those players.
        :param players: The list the players should be added to.
        :type players: List[Player.Player]
        """
        message: str = 'How many AI players do you want to play with you? '
        error_message: str = 'You must provide a valid players amount!'
        player_count: int = Utils.Utils.prompt_number(message, error_message)
        # Get next index in order to assign a color to the player.
        current_index: int = len(players) + 1
        for player_number in range(player_count):
            # Generate a name for the player and then initialize it.
            player_name: str = 'Player ' + str(current_index) + ' (AI)'
            player: Player = Player(player_name, Player.get_color_number(current_index), False)
            players.append(player)
            current_index += 1

    @staticmethod
    def __size_to_score(size: int) -> int:
        """
        Returns the score that should be assigned according to a given series size.
        :param size: The series size.
        :type size: int
        :return: The assigned score.
        :rtype: int
        """
        score: int = 0
        if size == 3:
            score = 2
        else:
            if size == 4:
                score = 10
            else:
                if size > 4:
                    score = 50
        return score

    @staticmethod
    def __compare_cell(cell_id: str, compare_cell_id: str, kind: int, owned: bool, series: List[Dict[str, int]]) -> int:
        """
        Compares the given cells according to the given series kind.
        :param cell_id: The string ID of the first cell to compare.
        :type cell_id: str
        :param compare_cell_id: The string ID of the second cell to compare.
        :type compare_cell_id: str
        :param kind: The series kind.
        :type kind: int
        :param owned: If the given player owns the first given cell.
        :type kind: bool
        :param series: The list of all the player's series currently active.
        :type kind: List[Dict[str, int]]
        :return: The score according to the series (if terminated).
        :rtype: int
        """
        score_to_add: int = 0
        if compare_cell_id in series[kind]:
            # A series is already present, check if it must be increased or terminated.
            if owned:
                # Keep the series going: update the last cell and increase its size.
                buffer: int = series[kind][compare_cell_id]
                del series[kind][compare_cell_id]
                series[kind][cell_id] = buffer + 1
            else:
                # Stop the series and compute the final series score.
                score_to_add = Player.__size_to_score(series[kind][compare_cell_id])
                del series[kind][compare_cell_id]
        else:
            # Start a new series.
            if owned:
                series[kind][cell_id] = 1
        return score_to_add

    def __init__(self, name: str, color: int, is_human: bool = True):
        """
        The class constructor.
        :param name: The player name.
        :type name: str
        :param color: The color assigned to the player as ANSI code.
        :type color: int
        :param is_human: If set to true it means this player is a human player.
        :type is_human: bool
        """
        self.__name = name
        self.__color = color
        self.__is_human = is_human
        self.__score = 0

    def set_name(self, name: str) -> None:
        """
        Sets the player name.
        :param name: The player name.
        :type name: str
        """
        self.__name = name

    def get_name(self) -> str:
        """
        Returns the player name.
        :return: The player name.
        :rtype: str
        """
        return self.__name

    def set_color(self, color: int) -> None:
        """
        Sets the player color.
        :param color: The color assigned to the player as ANSI code.
        :type color: int
        """
        self.__color = color

    def get_color(self) -> int:
        """
        Returns the player color.
        :return: The color assigned to the player as ANSI code.
        :rtype: int
        """
        return self.__color

    def set_is_human(self, is_human: bool) -> None:
        """
        Sets if this player is a human player or not.
        :param is_human: If set to true it means that this player is a human player.
        :type is_human: bool
        """
        self.__is_human = is_human

    def get_is_human(self) -> bool:
        """
        Returns if this player is a human player or not.
        :return: If this player is a human player will be returned true.
        :rtype: bool
        """
        return self.__is_human

    def get_score(self) -> int:
        """
        Returns this player's score.
        :return: This player's score.
        :rtype: int
        """
        return self.__score

    def get_marker(self) -> str:
        """
        Returns this player's marker as an ANSI string.
        :return: This player's marker.
        :rtype: str
        """
        return '\033[' + str(self.__color) + 'm ██ \033[0m'

    def compute_score(self, matrix) -> int:
        """
        Computes this player's score.
        :param matrix: The game matrix being used.
        :type matrix: Matrix.Matrix
        :return: The computed score.
        :rtype: int
        """
        score: int = 0
        size: int = matrix.get_size()
        series: List[Dict[str, int]] = [{}, {}, {}, {}]
        # Iterate the whole game matrix.
        for row in range(size):
            for column in range(size):
                # Get the player who occupies this cell.
                value: Optional[Player] = matrix.get_cell((row, column))
                owned: bool = False
                # Check if this cell's owner is the player represented by this class instance.
                if value is not None and value.get_name() is self.__name:
                    owned = True
                # Generate an unique cell ID represented as a string.
                cell_id: str = str(row) + ',' + str(column)
                # Compute any kind of series allowed.
                for kind in range(4):
                    if kind == 0:
                        # Check if this cell belongs to a vertical (|) series.
                        compare_cell_id: str = str(row) + ',' + str(column - 1)
                        score = score + Player.__compare_cell(cell_id, compare_cell_id, kind, owned, series)
                    else:
                        if kind == 1:
                            # Check if this cell belongs to a horizontal (-) series.
                            compare_cell_id: str = str(row - 1) + ',' + str(column)
                            score = score + Player.__compare_cell(cell_id, compare_cell_id, kind, owned, series)
                        else:
                            if kind == 2:
                                # Check if this cell belongs to a left-diagonal (\) series.
                                compare_cell_id: str = str(row - 1) + ',' + str(column + 1)
                                score = score + Player.__compare_cell(cell_id, compare_cell_id, kind, owned, series)
                            else:
                                if kind == 3:
                                    # Check if this cell belongs to a right-diagonal (/) series.
                                    compare_cell_id: str = str(row - 1) + ',' + str(column - 1)
                                    score = score + Player.__compare_cell(cell_id, compare_cell_id, kind, owned, series)
        # Iterate any kind of series allowed and sum the scores.
        for series_group in series:
            for cell_id in series_group:
                if series_group[cell_id] > 2:
                    score = score + Player.__size_to_score(series_group[cell_id])
        self.__score = score
        return score
