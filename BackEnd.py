WHITE_KING_MOVED = False
BLACK_KING_MOVED = False
BLACK_LEFT_ROOK_MOVED = False
BLACK_RIGHT_ROOK_MOVED = False
WHITE_LEFT_ROOK_MOVED = False
WHITE_RIGHT_ROOK_MOVED = False
"""
all the above values are for determining whether these pieces moved or not in order to know if castling can be performed"""
WHITE_DOWN = True # white pieces are positioned at the bottom of the board or not

# These values are for testing. Allows me to easily initiate all the boards with the king/rook already seen as moved
# so that castling cannot be done when testing custom boards

test_board = [
            ['□□', '□□', 'bq', '□□', 'bk', '□□', '□□', '□□'],
            ['br', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # black pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # '□□' means empty square
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', 'wk', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # white pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            [[True, True, True],
             [True, True, True], (-1, -1), WHITE_DOWN]
]
test_board2 = [
            ['□□', '□□', '□□', '□□', 'bk', '□□', '□□', '□□'],
            ['□□', '□□', 'br', '□□', '□□', '□□', '□□', '□□'],  # black pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # '□□' means empty square
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', 'wp', '□□', 'wk', '□□', '□□', '□□'],
            ['□□', '□□', 'wr', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # white pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            [[True, True, True],
             [True, True, True], (-1, -1), WHITE_DOWN]
]
test_board3 = [
            ['□□', '□□', 'br', '□□', 'bk', '□□', '□□', '□□'],
            ['□□', '□□', 'br', '□□', '□□', '□□', '□□', '□□'],  # black pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # '□□' means empty square
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', 'wp', '□□', 'wk', '□□', '□□', '□□'],
            ['□□', '□□', 'wr', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # white pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            [[True, True, True],
             [True, True, True], (-1, -1), WHITE_DOWN]
]


class Logic:
    def __init__(self, dimension):
        """
        :param dimension: the number of squares both horizontally and vertically
        """
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],  # black pieces
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],  # '□□' means empty square
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['□□', '□□', '□□', '□□', '□□', '□□', '□□', '□□'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],  # white pieces
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
            [[WHITE_LEFT_ROOK_MOVED, WHITE_KING_MOVED, WHITE_RIGHT_ROOK_MOVED],
             [BLACK_LEFT_ROOK_MOVED, BLACK_KING_MOVED, BLACK_RIGHT_ROOK_MOVED], (-1, -1), WHITE_DOWN]  # (Left Rook moved / King moved / Right Rook moved) for each color / Last double pawn move made coordinates
        ]    #                                                        double pawn last move coordinates, white pieces are down
        self.dimension = dimension
        self.draw_by_repetition = False
        self.board_history = [test_board]
        self.promotion_chosen_piece = '□□'
        self.promotion_board = self.initialize_empty_board()
        self.promotion_screen = False
        self.promotion_row = -1
        self.promotion_column = -1
        self.future_board = self.initialize_empty_board()
        self.checkmated = False
        self.stalemated = False
        self.piece_selected = False
        self.selected_square_row = 0
        self.selected_square_column = 0
        self.selected_square_value = ''
        self.move_number = 1
        self.turn = True  # True means white to move and False means black to move
        self.square_size = 0

    def move_or_select_piece(self, board, location, square_size, piece_selected, turn, ai):
        """
        makes the actual move if a piece is selected, otherwise selects a piece
        :param board: the logical board
        :param location: the row and column in a tuplet
        :param square_size: the size of the square, for flexibility
        """
        self.square_size = square_size
        column = location[0]
        row = location[1]
        square_value = (board[row])[column]
        if not piece_selected and not ai:
            if square_value != '□□':
                if (turn and square_value[0] == 'w') or (not turn and square_value[0] == 'b'):
                    self.select_piece(board, row, column)
                    # main.draw_possible_moves(screen, current_board, raw_to_matrix(raw_location)[0],
                                        # raw_to_matrix(raw_location)[1])

        elif square_value[0] == self.selected_square_value[0] and not ai:
            self.select_piece(board, row, column)
        else:
            f_board = self.verify_move_final(board, row, column, self.selected_square_row, self.selected_square_column, ai, True)
            if f_board:
                self.transfer_board(board, f_board)
                self.move_number += 1
                self.piece_selected = False
                self.board_history.append(f_board)
                self.transfer_board(self.board, board)
                self.transfer_board(test_board, self.board)
                # making the move itself
                self.turn = not self.turn
                color = 'w' if self.turn else 'b'
                if self.checkmate(board, color) == 1:
                    self.checkmated = True
                    print('CHECKMATE')
                elif self.checkmate(board, color) == 2:
                    self.stalemated = True
                    print('STALEMATE')
                elif len(self.board_history) > 8:
                    if self.board_equals(self.board_history[-1], self.board_history[-5], self.board_history[-9]):
                        self.draw_by_repetition = True
                return True
        return False

    def select_piece(self, board, row, column):
        self.piece_selected = True
        self.selected_square_row = row
        self.selected_square_column = column
        self.selected_square_value = (board[row])[column]

    def checkmate(self, board, color):
        """after each move, we call this function to verify if it's checkmate, stalemate or neither
        :param board: the logical board
        :param color: the color of the pieces that we need to verify"""
        checkmate_board = self.initialize_empty_board()
        self.transfer_board(checkmate_board, board)
        for piece in self.find_color_pieces(checkmate_board, color):
            for search_row in range(self.dimension):
                for search_column in range(self.dimension):
                    if self.verify_move_final(checkmate_board, search_row, search_column, piece[0], piece[1], True, False):
                        return 0  # NOT CHECKMATE
        (king_row, king_column) = self.find_king(board, color)
        if self.verify_piece_attacked(board, king_row, king_column, ((board[king_row])[king_column])[0]):
            return 1  # CHECKMATE
        else:
            return 2  # STALEMATE

    def board_equals(self, board1, board2, board3):
        """used for draw by repetition, to check if the same position is reached three times in a row
        :param board1: the first board we compare
        :param board1: the fifth board we compare
        :param board1: the ninth board we compare"""
        for row in range(self.dimension):
            if not(board1[row] == board2[row] == board3[row]):
                return False
        return True

    def print_board(self, board):
        for row in board:
            print(row)
        print('------------------')

    def verify_move_final(self, board, row, column, initial_row, initial_column, ai, actual_move):
        """after verifying if a move is legal from a basic point of view, we need to do additional checks, such as
        ally king being under attack after the move, activating the promotion board if necessary.
        After all these checks, the updated board is returned if the move is legal, otherwise the function returns False
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location"""
        future_board = self.initialize_empty_board()  # Used to verify if moving a piece will leave its king exposed
        self.transfer_board(future_board, board)
        if self.verify_move(future_board, row, column, initial_row, initial_column):
            (future_board[row])[column] = (future_board[initial_row])[initial_column]
            (future_board[initial_row])[initial_column] = '□□'
            # making the move on the future board to check if the king will be under attack after it
            (king_row, king_column) = self.find_king(future_board, (future_board[row])[column][0])
            # finding the king of the same color as the selected piece

            if not self.verify_piece_attacked(future_board, king_row, king_column, ((future_board[king_row])[king_column])[0]):

                for search_column in range(self.dimension):
                    if (future_board[7 * (not WHITE_DOWN)])[search_column] == 'wp':
                        if not ai:
                            if actual_move:
                                self.promotion(board, 7 * (not WHITE_DOWN), search_column, initial_row, initial_column)
                        else:
                            (future_board[7 * (not WHITE_DOWN)])[search_column] = 'wq'
                    if (future_board[7 * WHITE_DOWN])[search_column] == 'bp':
                        if not ai:
                            if actual_move:
                                self.promotion(board, 7 * WHITE_DOWN, search_column, initial_row, initial_column)
                        else:
                            (future_board[7 * WHITE_DOWN])[search_column] = 'bq'
                if (future_board[row])[column] == 'wk':
                    ((future_board[self.dimension])[0])[1] = True
                if (future_board[row])[column] == 'bk':
                    ((future_board[self.dimension])[1])[1] = True
                    """updating the board info if the king has moved"""
                return future_board
        return False

    def verify_move(self, board, row, column, initial_row, initial_column):
        """here we do basic validations for each king of piece
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location"""
        row_distance = row - initial_row
        column_distance = column - initial_column
        chosen_piece = ((board[initial_row])[initial_column])[1]
        chosen_piece_color = ((board[initial_row])[initial_column])[0]
        if row < 0 or row > 7 or column < 0 or column > 7:
            return False
        # in case that the move is out of bounds, could happen when automatically attempting or checking moves
        if self.draw_by_repetition:
            return False
        if chosen_piece_color == ((board[row])[column])[0]:
            return False
        """can't capture its ally"""
        if chosen_piece == 'n':  # ------------KNIGHT------------
            if ((abs(row_distance) + abs(column_distance)) == 3) and ((abs(row_distance) * abs(column_distance)) == 2):
                (board[self.dimension])[2] = (-1, -1) # resetting en passant
                return True

        elif chosen_piece == 'p':  # ------------PAWN--------------
            if initial_row == 7 or initial_row == 0:
                return False
            last_double_pawn_move = (board[self.dimension])[2]
            if chosen_piece_color == 'w':  # --------WHITE
                if row_distance == -1 + ((not WHITE_DOWN) * 2) and abs(column_distance) == 1:  # capturing
                    if (board[row])[column] != '□□':
                        return True
                    if last_double_pawn_move == (row + (1 - ((not WHITE_DOWN) * 2)), column):  # en passant
                        (board[row + 1 - ((not WHITE_DOWN) * 2)])[column] = '□□'  # one of two exceptions when i modify the board while verifying
                        return True  # because it's the only move that doesn't capture on the square where it's moving

                if (board[initial_row - 1 + (not WHITE_DOWN) * 2])[column] != '□□':
                    return False
                if row_distance == -1 + ((not WHITE_DOWN) * 2) and column == initial_column:
                    (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                    return True

                if initial_row == (7 * WHITE_DOWN) - 1 + ((not WHITE_DOWN) * 2):  # if initial row, it can move two squares
                    if (row_distance == -2 + ((not WHITE_DOWN) * 4)) and column_distance == 0 and (board[row])[column] == '□□':
                        (board[self.dimension])[2] = (row, column)  # updating the board info of the last double move
                        return True

            else:                          # --------BLACK
                if row_distance == 1 - ((not WHITE_DOWN) * 2) and abs(column_distance) == 1:  # capturing
                    if (board[row])[column] != '□□':
                        return True
                    if last_double_pawn_move == (row - 1 + ((not WHITE_DOWN) * 2), column):  # en passant
                        (board[row - 1 + ((not WHITE_DOWN) * 2)])[column] = '□□'  # the only exception when i modify the board while verifying,
                        (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                        return True   # because it's the only move that doesn't capture on the square that's it's moving
                if (board[initial_row + 1 - (not WHITE_DOWN) * 2])[column] != '□□':
                    return False
                if row_distance == 1 - ((not WHITE_DOWN) * 2) and column == initial_column:
                        (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                        return True

                if initial_row == (7 * (not WHITE_DOWN)) - 1 + (WHITE_DOWN * 2):

                    if (row_distance == 2 - ((not WHITE_DOWN) * 4)) and column_distance == 0 and (board[row])[column] == '□□':
                        (board[self.dimension])[2] = (row, column)  # updating the board info of the last double move
                        return True

        elif chosen_piece == 'k':  # ------------KING------------
            if abs(row_distance) < 2 and abs(column_distance) < 2:
                if chosen_piece_color == 'w':
                    ((board[self.dimension])[0])[1] = True  # notifying the board that the white king has moved and cant castle anymore
                elif chosen_piece_color == 'b':           # the main board will be updated with this information only after the final_check_verification returns True
                    ((board[self.dimension])[1])[1] = True
                (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                return True

            if chosen_piece_color == 'w' and not ((board[self.dimension])[0])[1]:
                if (row, column) == ((7 * WHITE_DOWN), 2) and not ((board[self.dimension])[0])[0]:  # white king big castle
                    pos1 = (board[row])[column - 1]
                    pos2 = (board[row])[column]
                    pos3 = (board[row])[column + 1]
                    if pos1 == '□□' and pos2 == '□□' and pos3 == '□□':
                        if not (self.verify_piece_attacked(board, row, column + 1, 'w') or self.verify_piece_attacked(board, row, column + 2, 'w')):
                            (board[7 * WHITE_DOWN])[3] = (board[7 * WHITE_DOWN])[0]  # considering that this is a special move where two pieces move at the same time, we will move one of them before the actual move happens
                            (board[7 * WHITE_DOWN])[0] = '□□'
                            (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                            return 2
                if (row, column) == (7 * WHITE_DOWN, 6) and not ((board[self.dimension])[0])[2]: # white king small castle
                    pos1 = (board[row])[column - 1]
                    pos2 = (board[row])[column]
                    if pos1 == '□□' and pos2 == '□□':
                        if not (self.verify_piece_attacked(board, row, column - 1, 'w') or self.verify_piece_attacked(board, row, column - 2, 'w')):
                            (board[7 * WHITE_DOWN])[5] = (board[7 * WHITE_DOWN])[7]  # considering that this is a special move where two pieces move at the same time, we will move one of them before the actual move happens
                            (board[7 * WHITE_DOWN])[7] = '□□'
                            ((board[self.dimension])[0])[1] = True
                            ((board[self.dimension])[0])[2] = True
                            (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                            return 2

            if chosen_piece_color == 'b' and not ((board[self.dimension])[1])[1]:
                if (row, column) == (7 * (not WHITE_DOWN), 2) and not ((board[self.dimension])[1])[0]:  # black king big castle
                    pos1 = (board[row])[column - 1]
                    pos2 = (board[row])[column]
                    pos3 = (board[row])[column + 1]
                    if pos1 == '□□' and pos2 == '□□' and pos3 == '□□':
                        if not (self.verify_piece_attacked(board, row, column + 1, 'b') or self.verify_piece_attacked(board, row, column + 2, 'b')):
                            (board[7 * (not WHITE_DOWN)])[3] = (board[7 * (not WHITE_DOWN)])[0]  # considering that this is a special move where two pieces move at the same time, we will move one of them before the actual move happens
                            (board[7 * (not WHITE_DOWN)])[0] = '□□'
                            ((board[self.dimension])[1])[1] = True
                            ((board[self.dimension])[1])[0] = True
                            (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                            return 2
                if (row, column) == (7 * (not WHITE_DOWN), 6) and not ((board[self.dimension])[1])[2]:  # black king small castle
                    pos1 = (board[row])[column - 1]
                    pos2 = (board[row])[column]
                    if pos1 == '□□' and pos2 == '□□':
                        if not (self.verify_piece_attacked(board, row, column - 1, 'b') or self.verify_piece_attacked(board, row, column - 2, 'b')):
                            (board[7 * (not WHITE_DOWN)])[5] = (board[7 * (not WHITE_DOWN)])[7]  # considering that this is a special move where two pieces move at the same time, we will move one of them before the actual move happens
                            (board[7 * (not WHITE_DOWN)])[7] = '□□'
                            ((board[self.dimension])[1])[1] = True
                            ((board[self.dimension])[1])[2] = True
                            (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                            return 2

        elif chosen_piece == 'r':  # ------------ROOK------------
            if self.rook_move_validity(board, row, column, initial_row, initial_column):
                if (initial_row, initial_column) == (7 * WHITE_DOWN, 0):  # left white rook
                    ((board[self.dimension])[0])[0] = True
                if (initial_row, initial_column) == (7 * WHITE_DOWN, 7):  # right white rook
                    ((board[self.dimension])[0])[2] = True
                if (initial_row, initial_column) == (7 * (not WHITE_DOWN), 0):  # left black rook
                    ((board[self.dimension])[1])[0] = True
                if (initial_row, initial_column) == (7 * (not WHITE_DOWN), 7):  # right black rook
                    ((board[self.dimension])[1])[2] = True
                (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                return True
            return False

        elif chosen_piece == 'b':  # ------------BISHOP------------
            if self.bishop_move_validity(board, row, column, initial_row, initial_column):
                (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                return True
            return False

        elif chosen_piece == 'q':  # ------------QUEEN------------
            # for the queen we just validate as for a rook and a bishop combined
            rook_validation = self.rook_move_validity(board, row, column, initial_row, initial_column)
            bishop_validation = self.bishop_move_validity(board, row, column, initial_row, initial_column)
            if rook_validation or bishop_validation:
                (board[self.dimension])[2] = (-1, -1)  # resetting en passant
                return True
            return False
        else:
            return False

    def verify_piece_attacked(self, board, row, column, piece_color):
        """used vor verifying if the king is under attack for certain moves: check by exposure, castling
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param piece_color: the color of the piece we need to verify on"""
        verification_board = self.initialize_empty_board()
        self.transfer_board(verification_board, board)
        for search_row in range(self.dimension):
            for search_column in range(self.dimension):
                if (((verification_board[search_row])[search_column])[0] != piece_color) and (((verification_board[search_row])[search_column])[0] != '□'):
                    if self.verify_move(verification_board, row, column, search_row, search_column):
                        return True
        return False

    def transfer_board(self, board1, board2):
        """transferring a board's contents to another, not very efficient
        :param board1: the board where the content is copied
        :param board2: the board from which the content is copied"""
        for search_row in range(self.dimension):
            for search_column in range(self.dimension):
                (board1[search_row])[search_column] = (board2[search_row])[search_column]
        for i in range(2):
            for j in range(3):
                ((board1[self.dimension])[i])[j] = ((board2[self.dimension])[i])[j]
        (board1[self.dimension])[2] = (board2[self.dimension])[2]
        (board1[self.dimension])[3] = (board2[self.dimension])[3]

    """def transfer_board_efficient(self, board2):
        board1 = list(board2)
        return board1"""

    def initialize_empty_board(self):
        future_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(self.dimension):
            future_board[i] = ['□□', '□□', '□□', '□□', '□□', '□□', '□□',
                               '□□']  # Used to verify if moving a piece will leave its king exposed
        future_board[self.dimension] = [[WHITE_LEFT_ROOK_MOVED, WHITE_KING_MOVED, WHITE_RIGHT_ROOK_MOVED],
                                        [BLACK_LEFT_ROOK_MOVED, BLACK_KING_MOVED, BLACK_RIGHT_ROOK_MOVED], (-1, -1), WHITE_DOWN]
        return future_board

    def find_king(self, board, color):
        """
        :param board: the logical board
        :param color: the color of the king that needs to be found
        """
        for search_row in range(self.dimension):  # finding the king of the chosen color
            for search_column in range(self.dimension):
                if ((board[search_row])[search_column])[1] == 'k' and \
                        ((board[search_row])[search_column])[0] == color:
                    king_row = search_row
                    king_column = search_column
        return king_row, king_column

    def rook_move_validity(self, board, row, column, initial_row, initial_column):
        """starting from the coordinates where we want to move the rook, we go backwards towards the rook and check
        if there are any pieces in the way. And the move must be either on the same column, or the same row
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location"""
        if column == initial_column:
            while (row != initial_row + 1) and (row != initial_row - 1):
                row = (row + 1 if row < initial_row else row - 1)
                if (board[row])[column] != '□□':
                    return False
            return True
        if row == initial_row:
            while (column != initial_column + 1) and (column != initial_column - 1):
                column = (column + 1 if column < initial_column else column - 1)
                if (board[row])[column] != '□□':
                    return False
            return True
        return False

    def bishop_move_validity(self, board, row, column, initial_row, initial_column):
        """
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location
        """
        row_distance = row - initial_row
        column_distance = column - initial_column
        #I have discovered that the math equation is simply that the row distance must be equal to the column one,
        #and again we go backwards towards the bishop and check if there is any piece in the way
        if abs(row_distance) == abs(column_distance):
            while (row != (initial_row + 1)) and (row != (initial_row - 1)):
                row = (row + 1 if row < initial_row else row - 1)
                column = (column + 1 if column < initial_column else column - 1)
                if (board[row])[column] != '□□':
                    return False
            return True
        return False

    def pawn_promotion(self, board, row, column, initial_row, initial_column):
        """promotion in the case of the ai, where it automatically gets a queen
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location"""
        pawn_color = ((board[initial_row])[initial_column])[0]
        if pawn_color == 'w' and (row == (not (board[self.dimension])[3]) * (self.dimension - 1)):
            (board[row])[column] = 'wq'
        elif pawn_color == 'b' and row == ((board[self.dimension])[3]) * (self.dimension - 1):
            (board[row])[column] = 'bq'

    def promotion(self, board, row, column, initial_row, initial_column):
        """creating the additional backend board that is used for displaying the promotion screen
        :param board: the logical board
        :param row: the row of the logical board location where the piece is to be moved
        :param column: the column of the logical board location where the piece is to be moved
        :param initial_row: the row of the initial piece location
        :param initial_column: the column of the initial piece location"""
        color = ((board[initial_row])[initial_column])[0]
        promotion_board = self.initialize_empty_board()
        self.transfer_board(promotion_board, board)
        possible_promotions = ['q', 'r', 'b', 'n']
        up_or_down = 1 if row == 0 else -1
        for i in range(4):
            (promotion_board[row + i*up_or_down])[column] = color + possible_promotions[i]
        self.transfer_board(self.promotion_board, promotion_board)
        self.promotion_row = row
        self.promotion_column = column
        self.promotion_screen = True

    def choose_promotion(self, board, location):
        """updating the backend board when a piece is selected in the promotion screen
        :param board: the logical board
        "param location: tuple of the row and column of the chosen promoted piece"""
        row = location[1]
        column = location[0]
        if column == self.promotion_column:
            if self.promotion_row == 0:
                if row < 4:
                    (board[self.promotion_row])[self.promotion_column] = (self.promotion_board[row])[column]
                    self.promotion_screen = False
                    return True
            if self.promotion_row == 7:
                if row >= 4:
                    (board[self.promotion_row])[self.promotion_column] = (self.promotion_board[row])[column]
                    self.promotion_screen = False
                    return True
        return False

    def find_color_pieces(self, board, color):  # returns the coordinates of the chosen color pieces
        """
        :param board: the logical board
        :param color: the color of the king that needs to be found
        """
        pieces_coordinates = []
        for search_row in range(self.dimension):
            for search_column in range(self.dimension):
                piece = (board[search_row])[search_column]
                if piece[0] == color:
                    pieces_coordinates.append((search_row, search_column))
        return pieces_coordinates

    def get_board(self):
        return self.board
