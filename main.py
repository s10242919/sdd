#SDD Assignment
#Elizabeth Tan, Yee Wan Sim, Shannen Pang, Nge Sin Yu
# import modules
import json
import jsonpickle
from math import floor
import random
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
        self._turn = 1

    @property
    def board(self):
        return self._board
    
    @board.setter
    def board(self, val):
        if not (isinstance(val, (Board))):
            raise TypeError(f"Expected Board, got {type(val)}")
        self._board = val

    @property
    def coins(self):
        return self._coins
    
    @coins.setter
    def coins(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"Expected int, got {type(val)}")
        self._coins = val

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"Expected int, got {type(val)}")
        self._score = val
    
    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, val):
        if not (isinstance(val, (int))):
            raise TypeError(f"Expected int, got {type(val)}")
        self._turn = val

    def incrementTurn(self):
        self._turn += 1

    # display menu
    def menu(self):
        options = {"Build a Building": self.build, 
                   "See Current Score": self.printScore,
                   "Save Game": self.save,
                   "Exit to Main Menu": self.exit}
        
        playing = True

        while playing:
            print(f"————— TURN {self.turn} —————")
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
            # call function
            function = list(options.values())[option]
            playing = function()
            #increment turn if build
            if (function == self.build):
                self.incrementTurn()


    def build(self):
        success = False
        numOptions = 2
        buildings = [Residential, Industry, Commercial, Park, Road]
        buildOptions = [building() for building in random.sample(buildings, numOptions)] 
        
        while not (success):
            print(f"Choose one from the following options: ")
            for idx, building in enumerate(buildOptions):
                print(f"{idx+1}. {building.name}")
            
            # get user's input
            while True:
                try:
                    option = int(input(f"Enter your option: "))
                except ValueError:
                    print("Please enter a number.")
                    continue
                if not (option-1 in range(numOptions)):
                    print("Please enter a valid option.")
                    continue
                else:
                    break
            # retrieve chosen building
            building = buildOptions[option-1]
            
            # get coords (validation in Board object)
            coord = input(f"Square to place {building.name} (e.g. F2): ")

            # check if user has enough coins
            if self.coins < building.cost:
                print(f"Not enough coins to build {building.name}.")
                continue

            if not (self.board.add(building, coord, self.turn == 1)):
                continue
            else:
                success = True
                self.coins -= building.cost
                self.score += building.calculatePoints()
                print(f"Current coins: {self.coins}")
                print(f"Current score: {self.score}")
                break

        # del remaining buildings
        for building in buildOptions:
            del building

        print()
        return True

    def printScore(self):
        print(f"Current score: {self.score}")
        return True

    def save(self):
        gameState = jsonpickle.encode(self)
        with open("save_game.json", "w") as write_file:
            json.dump(gameState, write_file)
        print("Game successfully saved!")
        return True

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
            return True
        print("Exiting game and returning to main menu...")
        return False
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
    def add(self, building, coord, firstTurn = False): # coord - coordinate
        if not (isinstance(building, (Building))):
            print("Not a valid building.")
            return False
        if not (isinstance(coord, (str)) and 
                (len(coord) >= 2) and 
                coord[0].isalpha() and 
                coord[1:].isdigit()):
            print("Not a valid coordinate. E.g. A19")
            return False

        # convert to uppercase
        coord = coord.upper()

        # check x & y coordinates (index value)
        x = ord(coord[0]) - ord("A")
        y = int(coord[1:]) - 1
        
        if not ((0 <= x <= (self.length-1)) and 0 <= y <= (self.length-1)):
            print("Coordinate not within boundaries.")
            return False
        
        # self._board[x][y]
        if isinstance(self.board[x][y], (Building)):
            print("Coordinate already occupied.")
            return False
        
        # check if turn is 1
        if not firstTurn:
            # make sure building is next to another building
            # check if adjacent squares are empty                
            if (
            (x == 0 and not (self._board[x][y-1] or self._board[x][y+1] or self._board[x+1][y]))
            or (x == self.length-1 and not (self._board[x][y-1] or self._board[x][y+1] or self._board[x-1][y]))
            or (y == 0 and not (self._board[x-1][y] or self._board[x+1][y] or self._board[x][y+1]))
            or (y == self.length-1 and not (self._board[x-1][y] or self._board[x+1][y] or self._board[x][y-1]))
            or (not (self._board[x-1][y] or self._board[x+1][y] or self._board[x][y-1] or self._board[x][y+1]))
            ):
                print("Building must be next to another building.")
                return False
                
        building.board = self
        self._board[x][y] = building
        print(f"{building.name} added to {coord}.")
        return True

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
    def calculatePoints(self):
        # each building has its own implementation
        pass


class Residential(Building):
    def __init__(self):
        super().__init__()
        self._character = "R"

    def calculatePoints(self):
        # if next to industry, 1 point only
        # else, 1 point for each adjacent residential or commercial
        # and 2 points for each adjacent park
        return 0


class Industry(Building):
    def __init__(self):
        super().__init__()
        self._character = "I"

    def calculatePoints(self):
        # 1 point per industry
        # generates 1 coin per adjacent residential
        return 0


class Commercial(Building):
    def __init__(self):
        super().__init__()
        self._character = "C"

    def calculatePoints(self):
        # 1 point per adjacent commercial
        # generates 1 coin per adjacent residential
        return 0


class Park(Building):
    def __init__(self):
        super().__init__()
        self._character = "O"

    def calculatePoints(self):
        # 1 point per adjacent park
        return 0


class Road(Building):
    def __init__(self):
        super().__init__()
        self._character = "*"

    def calculatePoints(self):
        # 1 point per connected road in the same row
        return 0
# end of 5 Buildings
# end of classes
    
# start of functions
# start new game
def newGame():
    # extra feature: get number of coins
    # get number of coins
    # while True:
    #     try:
    #         coins = int(input(f"Enter number of coins (10-50): "))
    #     except ValueError:
    #         print("Please enter a number.")
    #         continue
    #     if not (10 <= coins <= 50):
    #         print("Please enter a valid number.")
    #         continue
    #     else:
    #         break
    # create game
    # game = Game(coins)
    # print(f"New game started with {coins} coins.")
    game = Game()
    return game

# load game
def load():
    try:
        with open("save_game.json", "r") as read_file:
            gameState = json.load(read_file)
        game = jsonpickle.decode(gameState)
        print("Game successfully loaded!")
        return game
    except FileNotFoundError:
        print("No saved game found.")
        return None

# display high scores
def displayScores():
    print(f"————— HIGH SCORES —————")
    # todo: display high scores
    print(f"———————————————————————")
    return True

def main():
    game = None
    while True:
        # display menu
        print(f"————— MAIN MENU —————")
        print(f"1. Start New Game")
        print(f"2. Load Saved Game")
        print(f"3. Display High Scores")
        print(f"4. Exit")
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
                if not (option in range(4)):
                    print("Please enter a valid option.")
                    continue
                else:
                    break
        # call function
        functions = [newGame, load, displayScores, exit]
        function = functions[option]
        if (function == exit):
            print(f"Exiting program...")
            function()
        elif (function == displayScores):
            function()
        elif (function == newGame):
            game = function()
        elif (function == load):
            game = function()
            if game == None:
                continue
        
        print()
        if game != None:
            # start game
            game.menu()

main()