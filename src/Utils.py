class Utils:
    @staticmethod
    def prompt_number(message: str, error_message: str, allow_zero: bool = True) -> int:
        """
        Prompt an integer number to the user.
        :param message: The message to display.
        :type message: str
        :param error_message: The message to display if the given number is invalid.
        :type error_message: str
        :param allow_zero: If set to true zero won't be accepted if given.
        :type allow_zero: bool
        :return: The user provided integer number.
        :rtype: int
        """
        print(message, end='')
        # Convert the user provided number into integer.
        try:
            player_count: int = int(input())
        except ValueError:
            print(error_message)
            return Utils.prompt_number(message, error_message)
        if player_count < 0:
            print(error_message)
            return Utils.prompt_number(message, error_message)
        if allow_zero is False and player_count == 0:
            print(error_message)
            return Utils.prompt_number(message, error_message)
        return player_count
