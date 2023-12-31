#SDD Assignment
#Elizabeth Tan, Yee Wan Sim, Shannen Pang, Nge Sin Yu

# import modules
import json
import random
from math import floor
from abc import ABC, abstractmethod

# classes
# Game class
class Game:
    _defaultCoins = 16
    
    def __init__(self, coins = _defaultCoins):
        self._board = Board()
        if not (isinstance(coins, (int)) and coins >= 10):
            raise ValueError(f"Expected positive int, got {coins}")
        self._coins = coins
        self._score = 0

    @property #class attibute 
    def board(self):
        return self._board

    @property
    def coins(self):
        return self._coins

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"Expected int, got {type(val)}")
        self._score = val

    # display menu
    def menu(self):
        options = {"Build a Building": self.build, 
                "See Current Score": self.printScore,
                "Save Game": self.save,
                "Exit to Main Menu": self.exit}
        
        # show board
        self._board.print()

        # show stats
        print(f"Coins: {self.coins}")

        print(f"————— GAME MENU —————")
        for idx, key in enumerate(options.keys()):
            print(f"{idx+1}. {key}")

        print(f"—————————————————————")
        # check if option chosen is valid
        while True:
                try:
                    option = int(input(f"Enter your option: "))
                except ValueError:
                    print("Please enter a number.")
                    continue
                # minus one to get index value
                option -= 1
                if not (option in range(len(options))):
                    print("Please enter a valid option.")
                    continue
                else:
                    break
        list(options.values())[option]()
        

    def build(self):
       buildingList = [Residential, Industry, Commercial, Park, Road]

       randomBuilding1 = random.randrange(0,5)
       randomBuilding2 = random.randrange(0,5)
       # ensure that both building option is not the same
       while (randomBuilding2 == randomBuilding1):
           randomBuilding2 = random.randrange(0,5)
       building = [buildingList[randomBuilding1], buildingList[randomBuilding2]]

       #print buildings and options
       print(f"——————BUILDINGS——————")
       print("R - Residential\nI - Industry\nC - Commercial\nO - Park\n* - Road")
       print("Building Options: \n1)", building[0]().character,"\n2)", building[1]().character)
       print(f"—————————————————————")

       #input building option and check if option is valid
       while True:
           try:
               building_option = int(input("Enter your option: "))
           except ValueError:
               print("Please enter a number (1 OR 2).")
               continue
           building_option -= 1
           if not (building_option in range(len(building))):
            print("Please enter a valid option.")
            continue
           else:
               building_option = building[int(building_option)]
               break
           
       #input placing option and check if option is valid
       while True:
           try:
               coord_input = (input("Place where? "))
               row=ord(coord_input[0].upper()) - ord('A') + 1
               if (len(coord_input) == 2):
                    column = int(coord_input[-1:])
               elif (len(coord_input) == 3):
                    column = int(coord_input[-2:])
               else:
                   column = None 
           except ValueError:
               print("Please enter a valid input.")
               continue
           if ((column > 20) or (column == None) or (row > 20)):
               print("Please enter a valid placing.")
               continue
           else:
               break
       coord = [row - 1,column - 1]
       self.board.add(building_option, coord)
       self._coins -= 1
       building_option().calculatePoints(coord)



    def printScore(self):
        print(f"Current score: {self.score}")

    def save(self):
        # things to save:
        #   1. board
        #   2. current score
        #   3. current coins 

        gameState = {
            "board": {
                "length": self.board.length,
                "corner": self.board.corner,
                "hor": self.board.hor,
                "ver": self.board.ver,
                "board": self.board.board
            },
            "coins": self.coins,
            "score": self.score
        }
        with open("save_game.json", "w") as write_file:
            json.dump(gameState, write_file)
        print("Game successfully saved!")
        return

    def exit(self):
        valid = False
        while not (valid):
            confirm = input("All progress will be lost. Confirm exit? (y/n): ")
            valid = confirm.lower() in ["y", "n"]
            if not (valid):
                print("Please enter a valid option.")
                continue

        if confirm.lower() == "n":
            print(f"Exit cancelled...")
            return False
        print("Exiting game and returning to main menu...")
        return True
# end of Game class
    
# board
class Board:
    # default board values
    _defaultLength = 20 # todo: change to 20
    _defaultCorner = "+"  # corner piece
    _defaultHor = "—"  # horizontal piece
    _defaultVer = "|"  # vertical piece
    _sqrWidth = 3  # square width

    def __init__(
        self,
        length=_defaultLength,
        corner=_defaultCorner,
        hor=_defaultHor,
        ver=_defaultVer,
    ):
        if not (isinstance(length, (int)) and length > 0):
             raise ValueError(f"length: Positive int expected, got {length}")
        self._length = length
        if not (isinstance(corner, (str)) and len(corner) == 1):
             raise ValueError(f"corner: Single char expected, got {corner}")
        self._corner = corner
        if not (isinstance(hor, (str)) and len(hor) == 1):
             raise ValueError(f"hor: Single char expected, got {hor}")
        self._hor = hor
        if not (isinstance(ver, (str)) and len(ver) == 1):
             raise ValueError(f"ver: Single char expected, got {ver}")
        self._ver = ver
        self._board = []
        for _boardRow in range(length):
            _boardCol = []
            for y in range(length):
                _boardCol.append(0)
            self._board.append(_boardCol)

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, val=_defaultLength):
        self._length = val

    @property
    def corner(self):
        return self._corner
    
    @corner.setter
    def corner(self, val=_defaultCorner):
        self._corner = val

    @property
    def hor(self):
        return self._hor
    
    @hor.setter
    def hor(self, val=_defaultHor):
        self._hor = val

    @property
    def ver(self):
        return self._ver
    
    @ver.setter
    def ver(self, val=_defaultVer):
        self._ver = val

    @property
    def board(self):
        return self._board

    # add building to board
    def add(self, building, coord): # coord - coordinate
        row = coord[0]
        col = coord[-1] or coord[-2]
        building.board = self
        self.board[row][col] = building()

    def print(self): # display board
        # required variables
        mid = floor(self._sqrWidth / 2)  # get center index to replace
        charOrd  = ord('A') - 1

        #display col numbers
        for rowIdx, row in enumerate(self._board):
            rowLength = len(row)
            #print col numbers
            if rowIdx == 0:
                print("   ", end="")
                for colIdx in range(len(row)):
                    print(
                        f" {' ' * mid}{colIdx + 1}{' ' * (self._sqrWidth - mid - len(str(colIdx+1)))}",
                        end="")
                    if (colIdx == rowLength - 1):
                        print("\n", end="")

            # horizontal line +---+---+ (first 20)
            print(
                f"   {(self._hor * self._sqrWidth).join(self._corner for col in range(rowLength+1))}"
            )

            # vertical line   |   |   |    
            charOrd += 1
            sqrText = ' ' * self._sqrWidth # text in square
            print(
                f" {chr(charOrd)} {self._ver}{self._ver.join(sqrText if col == 0 else f'{sqrText[:mid]}{col.character}{sqrText[mid + 1:]}' for col in row)}{self._ver}"
            )
            # last horizontal line +---+---+
            if rowIdx == rowLength - 1:
                print(
                    f"   {(self._hor * self._sqrWidth).join(self._corner for col in range(rowLength+1))}"
                )


# end of Board


# 5 Buildings
class Building(ABC):
    def __init__(self):
        self._cost = 1
        self._points = 0
        
    @property
    def name(self):
        return self.__class__.__name__

    # cost of building
    @property
    def cost(self):
        return self._cost
    
    # cost setter

    @cost.setter
    def cost(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"{type(val)} not allowed. Int expected.")
        self._cost = val
    
    # points earned by building
    @property
    def points(self):
        return self._points
    
    # points setter
    @points.setter
    def points(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"{type(val)} not allowed. Int expected.")
        self._points = val
        
    # board
    @property
    def board(self):
        return self._board
    
    # board setter
    @board.setter
    def board(self, board):
        if not (isinstance(board, (Board))):
            raise TypeError(f"{type(board)} not allowed. Board expected.")
        self._board = board

    # character that represents building (abstract)
    @property
    def character(self):
        return self._character

    # abstract method to calculatePoints
    @abstractmethod
    def calculatePoints(self,coord):
        # each building has its own implementation
        pass


class Residential(Building):
    def __init__(self):
        super().__init__()
        self._character = "R"

    def calculatePoints(self,coord):
        # if next to industry, 1 point only
        # else, 1 point for each adjacent residential or commercial
        # and 2 points for each adjacent park

        # get placing of current building
        row = int(coord[0])
        col = int(coord[1])

        # get what is in the surrounding cells 
        if (row == 0):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = None
            down = self.board.board[row+1][col]
        elif (row == 19):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = None
        elif (col == 0):
            left = None
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        elif (col == 19):
            left = self.board.board[row][col-1]
            right = None
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        else:
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]

        # check if next to building
        # if not == 0 means there is a building 

        # turn True if there is already an Industry 
        haveI = False
        # left cell
        if not (left == 0 or left == None):
            # if next to industry/residential/commercial +1
            if (left.character == "I" and haveI == False):
                self._points += 1
                haveI = True
            if (left.character == "R" or left.character == "C"  ):
                self._points += 1
            elif (left.character == "O"):
                self._points += 2

        # right cell
        if not (right == 0 or right == None):
            # if next to industry/residential/commercial +1
            if (right.character == "I" and haveI == False):
                self._points += 1
                haveI = True
            if (left.character == "R" or left.character == "C"):
                self._points += 1
            elif (right.character == "O"):
                self._points += 2

        # upper cell
        if not (up == 0 or up == None):
            # check if next to residential/commercial +1
            if (up.character == "R" or up.character == "C"):
                self._points += 1
            elif (up.character == "O"):
                self._points += 2

        # bottom cell
        if not (down == 0 or down == None):
            # check if next to residential/commercial +1
            if (down.character == "R" or down.character == "C"):
                self._points += 1
            elif (down.character == "O"):
                self._points += 2


class Industry(Building):
    def __init__(self):
        super().__init__()
        self._character = "I"
    def calculatePoints(self,coord):
        # 1 point per industry
        self._points += 1
        # generates 1 coin per adjacent residential
        
        # get placing of current building
        row = int(coord[0])
        col = int(coord[1])

        # get what is in the surrounding cells 
        if (row == 0):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = None
            down = self.board.board[row+1][col]
        elif (row == 19):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = None
        elif (col == 0):
            left = None
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        elif (col == 19):
            left = self.board.board[row][col-1]
            right = None
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        else:
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]

        # check if next to building
        # if not == 0 means there is a building 

        # left cell
        if not (left == 0 or left == None):
            # check if next to residential
            if (left.character == "R"):
                self._coins += 1

        # right cell
        if not (right == 0 or right == None):
            # check if next to residential
            if (right.character == "R"):
                self._coins += 1

        # upper cell
        if not (up == 0 or up == None):
            # check if next to residential
            if (up.character == "R"):
                self._coins += 1

        # bottom cell
        if not (down == 0 or down == None):
            # check if next to residential
            if (down.character == "R"):
                self._coins += 1


class Commercial(Building):
    def __init__(self):
        super().__init__()
        self._character = "C"

    def calculatePoints(self,coord):
        # 1 point per adjacent commercial
        # generates 1 coin per adjacent residential
        
        # get placing of current building
        row = int(coord[0])
        col = int(coord[1])

        # get what is in the surrounding cells 
        if (row == 0):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = None
            down = self.board.board[row+1][col]
        elif (row == 19):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = None
        elif (col == 0):
            left = None
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        elif (col == 19):
            left = self.board.board[row][col-1]
            right = None
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        else:
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]

        # check if next to building
        # if not == 0 means there is a building 

        # left cell
        if not (left == 0 or left == None):
            # check if next to commercial
            if (left == "C"):
                self._points += 1
            if (left == "R"):
                self._coins += 1

        # right cell
        if not (right == 0 or right == None):
            if (right == "C"):
                self._points += 1
            if (right == "R"):
                self._coins += 1

        # upper cell
        if not (up == 0 or up == None):
            if (up == "C"):
                self._points += 1
            if (up == "R"):
                self._coins += 1

        # bottom cell
        if not (down == 0 or down == None):
            if (down == "C"):
                self._points += 1
            if (down == "R"):
                self._coins += 1

class Park(Building):
    def __init__(self):
        super().__init__()
        self._character = "O"

    def calculatePoints(self,coord):
        # 1 point per adjacent park
        
        # get placing of current building
        row = int(coord[0])
        col = int(coord[1])

        # get what is in the surrounding cells 
        if (row == 0):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = None
            down = self.board.board[row+1][col]
        elif (row == 19):
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = None
        elif (col == 0):
            left = None
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        elif (col == 19):
            left = self.board.board[row][col-1]
            right = None
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]
        else:
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]
            up = self.board.board[row-1][col]
            down = self.board.board[row+1][col]

        # check if next to building
        # if not == 0 means there is a building 

        # left cell
        if not (left == 0 or left == None):
            # check if next to park
            if (left == "O"):
                self._points += 1

        # right cell
        if not (right == 0 or right == None):
            # check if next to park
            if (right == "O"):
                self._points += 1

        # upper cell
        if not (up == 0 or up == None):
            # check if next to park
            if (up == "O"):
                self._points += 1

        # bottom cell
        if not (down == 0 or down == None):
            # check if next to park
            if (down == "O"):
                self._points += 1


class Road(Building):
    def __init__(self):
        super().__init__()
        self._character = "*"

    def calculatePoints(self,coord):
        # 1 point per connected road in the same row
        
        # get placing of current building
        row = int(coord[0])
        col = int(coord[1])

        # get what is in the surrounding cells 
        if (col == 0):
            left = None
            right = self.board.board[row][col+1]

        elif (col == 19):
            left = self.board.board[row][col-1]
            right = None

        else:
            left = self.board.board[row][col-1]
            right = self.board.board[row][col+1]


        # check if next to building
        # if not == 0 means there is a building 

        # left cell
        if not (left == 0 or left == None):
            # check if next to road
            if (left.character == "*"):
                self._points += 1
        # right cell
        if not (right == 0 or right == None):
            # check if next to road
            if (right.character == "*"):
                self._points += 1

# end of 5 Buildings
# end of classes
    
# start of functions
def main():

    # start new game
    def start_new_game():
        game = Game() # default: 16 coins
        while True:
            game.menu()

    # load saved game
    def load_saved_game():
        try:
            with open("save_game.json", "r") as read_saved:
                saved_game = json.load(read_saved)

                # get data from file
                saved_board = saved_game.get("board")
                saved_coins = saved_game.get("coins")
                saved_score = saved_game.get("score")

                # new Game instance 
                loaded_game = Game(coins = saved_coins)
                loaded_game.score = saved_score

                # new Board instance
                loaded_board = Board(
                length = saved_board.get("length", Board._defaultLength),
                corner = saved_board.get("corner", Board._defaultCorner),
                hor = saved_board.get("hor", Board._defaultHor),
                ver = saved_board.get("ver", Board._defaultVer)
                )
                loaded_board.board = saved_board.get("board", [])

                # set the loaded board to the loaded game
                loaded_game.board = loaded_board

                print("Game successfully loaded!")
                loaded_game.menu()  # start the loaded game

        except FileNotFoundError:
            print("No saved game.")

        except Exception as e:
            print(f"Error: {e}")

    # create main menu 
    while True:
        print("------------ Main Menu ------------")
        print("1. Start New Game")
        print("2. Load Saved Game")
        print("3. Display High Scores")
        print("4. Exit Game")

        choice = input("Enter your option [1-4]: ")
        if choice == '1':
            start_new_game()
        elif choice == '2':
            load_saved_game()
        elif choice == '3':
            display_high_scores()
        elif choice == '4':
            print("Exit game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            

main()