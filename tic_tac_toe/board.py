from copy import deepcopy
from tic_tac_toe.tree import Node, Tree


class Board:
    "Represent board in tic tac toe game"

    def __init__(self):
        self.board = [[None for i in range(3)] for i in range(3)]
        self.last_move = None
        self.last_sign = None

    def have_winner(self):
        "Checks if winner appeared."
        if self.last_move is None: return False
        row = self.last_move[0]
        col = self.last_move[1]

        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.last_sign:
            return True

        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.last_sign:
            return True

        first_diagonal = row == col
        second_diagonal = row + col == 2

        if first_diagonal:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.last_sign:
                return True

        if second_diagonal:
            if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.last_sign:
                return True

        return False

    def is_draw(self):
        "Checks if game is played in draw."
        if not self.available_moves() and not self.have_winner():
            return True
        return False

    def make_move(self, move, mark):
        "Make move."
        self.board[move[0]][move[1]] = mark
        self.last_move = move
        self.last_sign = mark

    def available_moves(self):
        "Returns list of the available moves"
        avail_list = []
        for key1, row in enumerate(self.board):
            for key2, elem in enumerate(row):
                if elem is None:
                    avail_list.append(tuple((key1, key2)))
        return avail_list

    def show(self):
        "Prints out board."
        print("\t\tBoard: \n")
        print("  A B C")

        for key1, row in enumerate(self.board):
            print(str(key1+1),end=' ')
            for key2, elem in enumerate(row):
                char = self.board[key1][key2]
                print(char if char is not None else " ", end=' ')
            print()


class Player:
    "Represent a tic tac toe player"

    def __init__(self, *args):
        if not args:
            self.name = input("Enter your name: ")
        else:
            self.name = args[0]

    def set_mark(self, char):
        "Set players mark."
        self.mark = char

    def make_move(self, board):
        "Makes move."
        try:
            move = input(("Please, {}, enter your move, like this 'A1': ").format(self.name))
            if len(move) != 2: raise ValueError("2 characters should be entered")
            if not move[0].isalpha(): raise ValueError("First character has to be letter.")
            if not move[1].isdigit(): raise ValueError("Second character has to be digit.")
            letter_A_ascii_code = 65
            move = tuple(((int(move[1]) - 1), ord(move[0].upper()) - letter_A_ascii_code))
            if not (0 <= move[0] < 3 and 0 <= move[1] < 3): raise ValueError("Move you've entered is out of the range.")
            if not move in board.available_moves(): raise ValueError("This move has been done earlier.")
            return move
        except ValueError as e:
            print(e)
            return self.make_move(board)


class AI_Bot(Player):
    def make_move(self, board):

        def rec_tree(board, node, depth=1):
            if board.have_winner():
                if board.last_sign == self.mark:
                    node.score = 100 / depth
                    return node.score
                else:
                    node.score = -100 / depth
                    return node.score
            if board.is_draw():
                node.score = 30 / depth
                return node.score
            for i in board.available_moves():
                temp_node = Node(i)
                node.children.append(temp_node)
            for i in node.children:
                temp_board = deepcopy(board)
                temp_board.make_move(i.data, mark=(self.mark if (depth % 2 == 0) else other_mark(self.mark)))
                rec_tree(temp_board, i, depth=depth + 1)
                node.score += i.score

            """
            board.show()
            print('t'*depth+str(node.score))
            return node.score
            """

        res_list = []

        for i in board.available_moves():
            temp_node = Node(i)
            temp_tree = Tree(temp_node)
            temp_board = deepcopy(board)
            temp_board.make_move(i, self.mark)
            rec_tree(temp_board, temp_node)
            res_list.append((temp_tree._root.data, temp_tree._root.score))

        """print(*res_list)"""
        return max(res_list, key=lambda x: x[1])[0]


def other_mark(mark):
    "Change the mark"
    return 'o' if mark == 'x' else 'x'
