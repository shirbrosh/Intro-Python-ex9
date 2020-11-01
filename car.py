class Car:
    """
    A class that defined a Car object, a pawn from the game 'rush-hour', each car has
    a name, length, location on the game board and orientation.
    """
    VERTICAL = 0
    HORIZONTAL = 1
    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        cor_lst = []
        row = self.__location[0]
        col = self.__location[1]
        length = self.__length
        if self.__orientation == Car.VERTICAL:
            for i in range(row, row + length):
                cor_lst.append((i, col))
        elif self.__orientation == Car.HORIZONTAL:
            for j in range(col, col + length):
                cor_lst.append((row, j))
        return cor_lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        movement_dict = {}
        if self.__orientation == Car.VERTICAL:
            movement_dict[Car.UP] = "the car can move in the up direction"
            movement_dict[Car.DOWN] = "the car can move in the down direction"
        elif self.__orientation == Car.HORIZONTAL:
            movement_dict[
                Car.RIGHT] = "the car can move in the right direction"
            movement_dict[Car.LEFT] = "the car can move in the left direction"
        return movement_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        cell_loc_lst = []
        cor_lst = self.car_coordinates()
        if movekey == Car.UP:
            cell_loc_lst.append((cor_lst[0][0] - 1, cor_lst[0][1]))
        elif movekey == Car.DOWN:
            cell_loc_lst.append((cor_lst[len(cor_lst) - 1][0] + 1,
                                 cor_lst[len(cor_lst) - 1][1]))
        elif movekey == Car.LEFT:
            cell_loc_lst.append((cor_lst[0][0], cor_lst[0][1] - 1))
        elif movekey == Car.RIGHT:
            cell_loc_lst.append((cor_lst[len(cor_lst) - 1][0],
                                 cor_lst[len(cor_lst) - 1][1] + 1))
        return cell_loc_lst

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        cell_loc_lst = self.movement_requirements(movekey)
        if self.__orientation == Car.VERTICAL:
            if movekey == Car.UP:
                self.__location = cell_loc_lst[0]
                return True
            elif movekey == Car.DOWN:
                self.__location = (
                    cell_loc_lst[0][0] - self.__length + 1, cell_loc_lst[0][1])
                return True
        elif self.__orientation == Car.HORIZONTAL:
            if movekey == Car.LEFT:
                self.__location = cell_loc_lst[0]
                return True
            elif movekey == Car.RIGHT:
                self.__location = (
                    cell_loc_lst[0][0], cell_loc_lst[0][1] - self.__length + 1)
                return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name



