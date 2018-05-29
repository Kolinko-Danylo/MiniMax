from tic_tac_toe.tree import Node, Tree
from tic_tac_toe.board import Board, Player, AI_Bot
from copy import deepcopy


class Game:
    "Represnt tic tac toe game"

    def __init__(self, player1, player2, board):
        self._player_list = [player1, player2]
        self._board = board
        self._current_player = 0

    def change_cur_player(self):
        "Change the current player(that who makes move)"
        if self._current_player == 0:
            self._current_player = 1
        else:
            self._current_player = 0

    def routine(self):
        "Process main routine"
        while not (self._board.have_winner() or self._board.is_draw()):
            self._board.show()
            cur_player = self._player_list[self._current_player]
            self._board.make_move(cur_player.make_move(deepcopy(self._board)), cur_player.mark)
            self.change_cur_player()
        self.change_cur_player()
        self._board.show()
        if self._board.is_draw():
            print("Draw. Friendship is winner.")
        else:
            print("Winner is {}.".format(self._player_list[self._current_player].name))


def main():
    "Sets up all main settings"
    pl1 = Player()
    pl2 = AI_Bot("me")
    pl1.set_mark('o')
    pl2.set_mark('x')
    board = Board()
    g = Game(pl1, pl2, board)
    g.routine()


if __name__ == "__main__":
    main()
