from car import Car


class Board:
    """
    A class that defined a Board object, a play board of the game 'rush-hour'. A
    board object contains the actual board- a list of lists, each list represent a
    row in the game board, and a car dictionary that keeps all the Cars objects that
    participate in the specific game.
    """
    LEN_BOARD = 7
    TARGET_CELL = (3, 7)
    EMPTY_CELL = "_"
    VERTICAL = 0
    HORIZONTAL = 1
    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"
    WARNING_MSG = {
        "vertical": "You cant move a vertical car right or left, chose a different direction",
        "horizontal": "You cant move a horizontal car up or down, chose a different "
                      "direction",
        "taken": "you cant move the car in this direction because the cell is already "
                 "taken",
        "out": "you are trying to move the car outside the board border"
        }

    def __init__(self):
        """
        A constructor for a Board object
        """
        board = []
        for i in range(0, self.LEN_BOARD):
            board_row = []
            for j in range(0, self.LEN_BOARD):
                board_row.append(self.EMPTY_CELL)
            board.append(board_row)
        self.__board = board
        self.__cars_dict = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_str = ""
        board = self.__board
        for i in range(0, len(board)):
            for j in range(0, len(board)):
                if j == len(board) - 1:
                    board_str += board[i][j] + "\n"
                else:
                    board_str += board[i][j] + " "
        return board_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cell_lst = []
        for row in range(0, self.LEN_BOARD):
            for col in range(0, self.LEN_BOARD):
                cell_lst.append((row, col))
        cell_lst.append(self.TARGET_CELL)
        return cell_lst

    def __wanted_cor_row_and_col(self, movekey, car):
        """A function that returns the cell location which must be empty for the car
        to move to the movekey direction- as a tuple, and also as integer that
        represents the row and column of the location"""
        wanted_cor = car.movement_requirements(movekey)[0]
        wanted_row = wanted_cor[0]
        wanted_col = wanted_cor[1]
        return wanted_cor, wanted_row, wanted_col

    def __in_range(self, wanted_cor):
        """A function that returns True if the given coordinate is in the board
        limits of False otherwise"""
        if wanted_cor in self.cell_list():
            return True
        return False

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        cars_dict = self.__cars_dict
        legal_moves_lst = []
        for car in cars_dict.values():
            move_dict = car.possible_moves()
            for key in move_dict.keys():
                wanted_cor, wanted_row, wanted_col = self.__wanted_cor_row_and_col(
                    key, car)
                coordinate = (wanted_row, wanted_col)
                if self.__in_range(wanted_cor) and self.cell_content(
                        coordinate) is None:
                    description = "you can move in the " + key + " direction"
                    legal_moves_lst.append((car.get_name(), key, description))
        return legal_moves_lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled
        for victory.
        :return: (row,col) of goal location
        """
        return self.TARGET_CELL

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row_cor = coordinate[0]
        col_cor = coordinate[1]
        if coordinate == self.TARGET_CELL:
            return None
        if self.__board[row_cor][col_cor] == self.EMPTY_CELL:
            return None
        else:
            return self.__board[row_cor][col_cor]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        cor_lst = car.car_coordinates()
        for cor in cor_lst:
            if not self.__in_range(cor) or self.cell_content(cor) is not None:
                return False
        self.__cars_dict[car.get_name()] = car
        cor_lst = car.car_coordinates()
        for cor in cor_lst:
            row = cor[0]
            col = cor[1]
            self.__board[row][col] = car.get_name()
        return True

    def __check_legal_move(self, wanted_car, movekey, need_to_be_empty):
        """A function that checks if a move is legal according to the game rules"""
        possible_moves_dict = wanted_car.possible_moves()
        for key in possible_moves_dict.keys():
            if key == self.RIGHT or key == self.LEFT:
                orientation = self.HORIZONTAL
            elif key == self.UP or key == self.DOWN:
                orientation = self.VERTICAL
        if orientation == self.VERTICAL and (
                movekey == self.RIGHT or movekey == self.LEFT):
            print(self.WARNING_MSG["vertical"])
            return False
        if orientation == self.HORIZONTAL and (
                movekey == self.UP or movekey == self.DOWN):
            print(self.WARNING_MSG["horizontal"])
            return False
        if self.cell_content(need_to_be_empty) is not None:
            print(self.WARNING_MSG["taken"])
            return False
        if not self.__in_range(need_to_be_empty):
            print(self.WARNING_MSG["taken"])
            return False
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        cars_dict = self.__cars_dict
        for car in cars_dict.values():
            if name == car.get_name():
                wanted_car = car
        need_to_be_empty = wanted_car.movement_requirements(movekey)[0]
        if self.__check_legal_move(wanted_car, movekey, need_to_be_empty):
            cord_lst = wanted_car.car_coordinates()
            row_empty = need_to_be_empty[
                0]  # the row of the coordinate to move
            col_empty = need_to_be_empty[
                1]  # the column of the coordinate to move
            if movekey == wanted_car.RIGHT or movekey == wanted_car.DOWN:
                # changing the first cell from the name to "_" and inserting the name
                # to the cell that needs to be empty
                row_first = cord_lst[0][0]  # the row of the first coordinate
                col_first = cord_lst[0][
                    1]  # the column of the first coordinate
                self.__board[row_first][col_first] = self.EMPTY_CELL
                self.__board[row_empty][col_empty] = name
            elif movekey == wanted_car.LEFT or movekey == wanted_car.UP:
                # the same change just the other way around- the last cell from the
                # name to "_" and inserting the name to the cell that needs to be
                # empty to the cell that needs to be empty
                row_last = cord_lst[len(cord_lst) - 1][
                    0]  # the row of the last coordinate
                col_last = cord_lst[len(cord_lst) - 1][
                    1]  # the column of the last coordinate
                self.__board[row_last][col_last] = self.EMPTY_CELL
                self.__board[row_empty][col_empty] = name
            wanted_car.move(movekey)
            return True
        return False
