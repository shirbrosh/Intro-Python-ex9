from board import Board
from car import Car
import helper
import sys

ALLOWED_COLORS = ["Y", "B", "O", "G", "W", "R"]
ALLOWED_DIRECTIONS = ["u", "d", "r", "l"]
MIN_CAR_LENGTH = 2
MAX_CAR_LENGTH = 4
MIN_ROW_COL = 0
MAX_ROW_COL = 6
VERTICAL = 0
HORIZONTAL = 1


class Game:
    """
    A class that defined a Game object, this Object runs the game 'rush-hour'.
    The game has a board which is a Board object and a car dictionary that keeps all
    the Cars objects that participate in the specific game.
    """
    INPUT_LEN = 3
    SEPARATE = ","
    RIGHT = 'r'
    CELL_TO_WIN1 = (3, 5)
    CELL_TO_WIN2 = (3, 6)
    MSGS = {
        "input": "\nPlease enter which car color would you like to move from the " \
                 "following:\nY, B, O, G, W, R.\nenter ',' and chose which direction " \
                 "would you like to move from the following:\nd- for down, u- for up," \
                 " r- for right and l- for left\n",
        "wrong input": "\n!!!!!!!!!!!\nyou have entered an invalid input, please " \
                       "re-enter\n!!!!!!!!!!!\n",
        "win": "\nyou won!!! congratulation :)",
        "start": "Welcome to rush hour game, this is your board:"
    }

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __check_valid_input(self, users_input):
        """A function that checks if the users input is valid according to the game
        requirements. It returns True if valid or False otherwise """
        # check if the input has 3 chars and the middle one is ',':
        if len(users_input) != self.INPUT_LEN or users_input[1] != self.SEPARATE:
            print(self.MSGS["wrong input"])
            return False
        users_input_lst = users_input.split(",")
        color = users_input_lst[0]
        movekey = users_input_lst[1]
        # check if the name and movekey are legal:
        if color not in ALLOWED_COLORS or movekey not in ALLOWED_DIRECTIONS:
            print(self.MSGS["wrong input"])
            return False
        return color, movekey

    def single_turn(self):
        """
        This function runs one round of the game :
            1. Gets the user's input of: what color car to move, and what
                direction to move it.
            2. Checks if the input is valid.
            3. Try moving car according to user's input or prints a suitable
        """
        print(self.__board)
        users_input = input(self.MSGS["input"])
        while not self.__check_valid_input(users_input):
            users_input = input(self.MSGS["input"])
        color, movekey = self.__check_valid_input(users_input)
        if self.__end_game(color, movekey):
            return True
        self.__board.move_car(color, movekey)
        return False

    def __end_game(self, color, movekey):
        """A function that determines if the player won the game- it checks if a car
        has reached the target location"""
        if movekey == self.RIGHT and self.__board.cell_content(
                self.CELL_TO_WIN1) == color and self.__board.cell_content(
                (self.CELL_TO_WIN2)) == color:
            return True
        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(self.MSGS["start"])
        while not self.single_turn():
            continue
        print(self.MSGS["win"])


def read_jason(game_board, filename):
    """A function that receives a file name for a jason file, opens, and reads the
    file and if all the information given in the file is valid according to the
    game rules, the data is updated to the game"""
    dict_game = helper.load_json(filename)
    for car, lst in dict_game.items():
        if car not in ALLOWED_COLORS:
            continue
        car_length = lst[0]
        if car_length < MIN_CAR_LENGTH or car_length > MAX_CAR_LENGTH:
            continue
        car_location = lst[1]
        car_location_row = car_location[0]
        car_location_col = car_location[1]
        if car_location_row < MIN_ROW_COL or car_location_row > MAX_ROW_COL or \
                car_location_col < MIN_ROW_COL or car_location_col > MAX_ROW_COL:
            continue
        car_orientation = lst[2]
        if car_orientation != HORIZONTAL and car_orientation != VERTICAL:
            continue
        car_to_add = Car(car, car_length, tuple(car_location), car_orientation)
        game_board.add_car(car_to_add)


if __name__ == "__main__":
    game_board = Board()
    filename = sys.argv[1]
    read_jason(game_board, filename)
    play_game = Game(game_board)
    play_game.play()
