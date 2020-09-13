from common.messages import GameMessage


class Game():
    def __init__(self):
        self.id = None

    def update(self, new_data: GameMessage):
        self.turn = new_data.turn
        self.board = new_data.board
        self.id = new_data.id
        self.name = new_data.name

    def render(self):
        if self.id is not None:
            print(f"Game: {self.name}({self.id})")
            print(f"Player {self.turn} is moving")
            print("")
            print("===========")
            print(f"[{self.board[0]}] [{self.board[1]}] [{self.board[2]}]")
            print(f"[{self.board[3]}] [{self.board[4]}] [{self.board[5]}]")
            print(f"[{self.board[6]}] [{self.board[7]}] [{self.board[8]}]")
            print("===========")
        else:
            print("Initializing game")
