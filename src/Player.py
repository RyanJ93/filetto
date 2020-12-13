from typing import List, Optional, Tuple


class Player:
    __name: str
    __color: int
    __is_human: bool
    __score: int

    @staticmethod
    def get_color_number(index: int) -> Optional[int]:
        colors: List[int] = [31, 32, 36, 34, 37]
        if index < len(colors):
            return colors[index]
        else:
            return None

    @staticmethod
    def pick_cord(matrix) -> Optional[Tuple[int, int]]:
        coords: Optional[Tuple[int, int]] = None
        if not matrix.is_full():
            size: int = matrix.get_size()
            for row in range(size):
                for column in range(size):
                    value: Optional[Player] = matrix.get_column((row, column))
                    if value is None:
                        coords = row, column
                        break
                if not coords:
                    break
        return coords

    def __init__(self, name: str, color: int, is_human: bool = True):
        self.__name = name
        self.__color = color
        self.__is_human = is_human
        self.__score = 0

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_color(self, color: int) -> None:
        self.__color = color

    def get_color(self) -> int:
        return self.__color

    def set_is_human(self, is_human: bool) -> None:
        self.__is_human = is_human

    def get_is_human(self) -> bool:
        return self.__is_human

    def get_score(self) -> int:
        return self.__score

    def get_marker(self) -> str:
        return '\033[' + str(self.__color) + 'm ██ \033[0m'

    def compute_score(self, matrix) -> int:
        score: int = 0
        size: int = matrix.get_size()

        for row in range(size):
            for column in range(size):
                value: Optional[Player] = matrix.get_column((row, column))
                # if value is not None and value.get_name() is self.__name:
        return score
