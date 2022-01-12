import random
import pygame as pyg
import time
import BackEnd
from BackEnd import *

WIDTH = HEIGHT = 1000
SQUARE_SIZE = HEIGHT//8
DIMENSION = 8
PICTURES = {}
PIECES = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
BROWN = (165, 42, 42, 255)
BEIGE = (246, 246, 227)
LIGHT_BLUE = (173, 216, 230)
FONT = 'Comic Sans MS'
TEXT_SIZE = 30
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
CIRCLE_WIDTH = 5
CIRCLE_COLOR = 'green'
AI_DEPTH = 2 # the actual depth is AI_DEPTH + 1
#TODO ADD CHECK CONCEPT TO AI ---- OPTIMIZE AI FOR LESS TIME CALCULATING ------ TIME PER MOVE
logic = Logic(DIMENSION)


def draw_board(screen):
    """drawing the basic board with no pieces
    :param screen: the actual "canvas" where everything is drawn"""

    colors = [pyg.Color('white'), pyg.Color(LIGHT_BLUE)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            pyg.draw.rect(screen, colors[(row + column) % 2],
                          pyg.Rect(SQUARE_SIZE * row, SQUARE_SIZE * column, SQUARE_SIZE, SQUARE_SIZE))


def draw_coordinates(p, screen, color):
    """
    :param p: the pygame object
    :param screen: the actual "canvas" where everything is drawn
    :param color: the color of the coordinates
    """
    p.font.init()
    my_font = p.font.SysFont(FONT, TEXT_SIZE - 10)
    for row in range(DIMENSION):
        text_surface = my_font.render(str(DIMENSION - row), False, color)
        screen.blit(text_surface, (5, row * SQUARE_SIZE))
        text_surface = my_font.render(str(LETTERS[row]), False, color)
        screen.blit(text_surface, ((row + 1) * (SQUARE_SIZE) - 10, (DIMENSION) * SQUARE_SIZE - 30))


def draw_pieces(screen, board):
    """
    :param screen: the actual "canvas" where everything is drawn
    "param board: the logical board
    """
    board_matrix = board
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board_matrix[row][column]
            if not piece == '□□':
                screen.blit(PICTURES[piece], ((SQUARE_SIZE * column) + 4, (SQUARE_SIZE * row) + 4))


def draw_circle(screen, row, column, color):
    """used for displaying the possible moves for each piece
    :param screen: the "canvas" on which everything is drawn
    :param row: the row of the circle
    :param column: the column of the circle
    :param color: the color of the circle
    """
    pyg.draw.circle(screen, color, ((SQUARE_SIZE * column) + SQUARE_SIZE/2,
                                    (SQUARE_SIZE * row) + SQUARE_SIZE/2), SQUARE_SIZE/4, CIRCLE_WIDTH)


def draw_rectangle(screen, row, column, color):
    """used for drawing the actual board
    :param screen: the "canvas" on which everything is drawn
    :param row: the row of the rectangle
    :param column: the column of the rectangle
    :param color: the color of the rectangle
    """
    pyg.draw.rect(screen, color,
                  pyg.Rect(SQUARE_SIZE * column, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))


def draw_promotion_rectangle(screen, promotion_row, promotion_column, color):
    """used for highlighting the selection squares in promotion screen
    :param screen: the "canvas" on which everything is drawn
    :param promotion_row: the row of the rectangle
    :param promotion_column: the column of the rectangle
    :param color: the color of the rectangle"""
    up_or_down = 1 if promotion_row == 0 else -1
    for i in range(4):
        draw_rectangle(screen, promotion_row + (i*up_or_down), promotion_column, color)


def write_game_finished(p, screen, color, finish_type):
    """when the game is over, we display the manner in which it has ended
    :param screen: the "canvas" on which everything is drawn
    :param color: the color of the text
    "param finish_type: in order to print the correct kind of """
    p.font.init()
    my_font = p.font.SysFont(FONT, TEXT_SIZE)
    if finish_type == 'checkmate':
        if not color:
            text_surface = my_font.render('WHITE WINS', False, BROWN)
        else:
            text_surface = my_font.render('BLACK WINS', False, BROWN)
    elif finish_type == 'stalemate':
        text_surface = my_font.render('STALEMATE', False, BROWN)
    else:
        text_surface = my_font.render('DRAW BY REPETITION', False, BROWN)
    screen.blit(text_surface, (((DIMENSION - 2) * SQUARE_SIZE / 2), (DIMENSION - 1) * SQUARE_SIZE / 2 + 10))


def load_images(p):
    """loading the actual piece images
    :param p: the pygame object"""
    for piece in PIECES:
        PICTURES[piece] = p.transform.scale(p.image.load('pieces_hd/' + piece + '.png'), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))


def dumb_ai(board, computer_turn):
    """simple ai that moves almost randomly
    :param board: the logical board
    :param computer_turn: to know if it is the computer's turn or not"""
    color = 'w' if computer_turn else 'b'
    while not(logic.checkmated or logic.stalemated or logic.draw_by_repetition):
        piece = random.choice(logic.find_color_pieces(board, color))
        logic.select_piece(board, piece[0], piece[1])
        for search_row in range(logic.dimension):
            for search_column in range(logic.dimension):
                if logic.verify_move_final(board, DIMENSION - search_row - 1, search_column, logic.selected_square_row, logic.selected_square_column, True, False):
                    logic.move_or_select_piece(board, (search_column, DIMENSION - search_row - 1), logic.square_size, logic.piece_selected, computer_turn, True)
                    return


def find_pieces_value(board, computer_turn):
    """returns the value of the opponent's pieces
    :param board: the logical board
    :param computer_turn: to know if it is the computer's turn or not"""
    pieces_color = 'w' if computer_turn else 'b'
    pieces_value = {(pieces_color + 'p') : 1, (pieces_color + 'n') : 3, (pieces_color + 'b') : 3, (pieces_color + 'r') : 5, (pieces_color + 'q') : 9, (pieces_color + 'k') : 0}
    pieces = logic.find_color_pieces(board, pieces_color)
    val_pieces = 0
    for enemy_piece in pieces:
        piece_value = (board[enemy_piece[0]])[enemy_piece[1]]
        val_pieces += pieces_value[piece_value]
    return val_pieces  # on a normal board, the maximum possible value is 39


def ai_check_mate(board, checkmate_moves, enemy_color, computer_turn):
    """in the case that ai does not have any move that gives it material advantage, it attempts to check mate by
    choosing moves that leave the enemy king with as few possible moves as possible
    :param board: the logical board
    :param computer_turn: to know if it is the computer's turn or not
    :param checkmate_moves: the moves given by the main ai that are do not result in material loss
    :param enemy_color: the color of the enemy pieces
    :param computer_turn: to know if it is the computer's turn or not
    """
    #TODO make it such that it prioritizes moves that don't lead to stalemate
    possible_moves_semi_coordinates = (-1, 0, 1)
    enemy_king_possible_moves = 9  # 8 is the actual maximum number of moves a king can perform
    best_move = (-1, -1, -1, -1)
    for move in checkmate_moves:
        potential_board = logic.verify_move_final(board, move[0], move[1], move[2], move[3], True, False)
        king_moves = 0
        enemy_king_coordinates = logic.find_king(potential_board, enemy_color)
        king_row, king_column = enemy_king_coordinates[0], enemy_king_coordinates[1]
        for row in possible_moves_semi_coordinates:
            for column in possible_moves_semi_coordinates:
                if logic.verify_move_final(potential_board, king_row + row, king_column + column,
                                           king_row, king_column, True, False):
                    king_moves += 1

        if king_moves < enemy_king_possible_moves:
            enemy_king_possible_moves = king_moves
            best_move = move

    if best_move[0] == -1:
        print("checkmate ai did not find any moves")
    logic.select_piece(board, best_move[2], best_move[3])
    logic.move_or_select_piece(board, (best_move[1], best_move[0]), logic.square_size, logic.piece_selected, computer_turn, True)


def print_smth(smth):
    print("smth")


def look_ahead_ai_v2(board, computer_turn, recursion):  # can also checkmate
    """This function goes through all the possible moves of itself and the opponent, with a customizable depth
    given by the "recursion" parameter and chooses the best one based only on material gain. By calling itself,
    it keps adding(for its own gains) and substracting(for its opponent's gains). The final value returned
    represents each "leaf" of the tree and it chooses the best one
    :param board: the logical board
    :param computer_turn: to know if it is the computer's turn or not
    :param recursion: so it can actually end at a certain depth, not go indefinitely"""
    enemy_color = 'b' if computer_turn else 'w'
    pieces_value = {(enemy_color + 'p'): 1, (enemy_color + 'n'): 3, (enemy_color + 'b'): 3, (enemy_color + 'r'): 5,
                    (enemy_color + 'q'): 9, (enemy_color + 'k'): 0}
    color = 'w' if computer_turn else 'b'
    starting_val_enemy_pieces = find_pieces_value(board, not computer_turn)
    best_value_captured = -50
    best_move = (-1, -1)
    best_move_piece = (-1, -1)
    checkmate_moves = []
    for piece in logic.find_color_pieces(board, color):
        for search_row in range(logic.dimension):
            for search_column in range(logic.dimension):
                """iterates through all the pieces and all their possible moves (iterates through 64 squares for each piece which is not efficient)"""
                potential_board = logic.verify_move_final(board, search_row, search_column, piece[0], piece[1], True,
                                                          False)
                """if the move is illegal, verify_move_final will return False, otherwise it will return a new board where the move was made"""
                if potential_board:
                    enemy_pieces = logic.find_color_pieces(potential_board, enemy_color)
                    potential_min_val_enemy_pieces = 0
                    for enemy_piece in enemy_pieces:
                        enemy_piece_value = (potential_board[enemy_piece[0]])[enemy_piece[1]]
                        potential_min_val_enemy_pieces += pieces_value[enemy_piece_value]
                        """we add up all the enemy pieces' values"""

                    value_captured = starting_val_enemy_pieces - potential_min_val_enemy_pieces
                    if recursion:
                        """goes to the next depth, calling itself but with a new board where the move was made, and simulates its own or the enemy's best move, depending on who's to move"""
                        next_depth_board = logic.initialize_empty_board()
                        logic.transfer_board(next_depth_board, potential_board)
                        possible_loss_value = look_ahead_ai(next_depth_board, not computer_turn, recursion - 1)
                        """by calling itself recursively, we can just subtract every value, considering that the 
                        ally capture values will become additions through the nature of recursion"""
                        value_captured -= possible_loss_value
                    """in case of not being able to capture anything, we add all the neutral moves in terms of material into a list so that we can use them for the checkmate function"""
                    if recursion == AI_DEPTH and value_captured == 0:
                        checkmate_moves.append((search_row, search_column, piece[0], piece[1]))

                    """here we update the value of the best move if that's the case, along with all its coordinates"""
                    if value_captured >= best_value_captured:
                        best_value_captured = value_captured
                        best_move_piece = (piece[0], piece[1])
                        best_move = (search_column, search_row)

    """if there is no material gain, we choose by using the check mate function, by choosing between all the moves that
    do not result in losing material, called "checkmate_moves" """
    if best_value_captured == 0 and recursion == AI_DEPTH:
        print('called checkmate')
        ai_check_mate(board, checkmate_moves, enemy_color, computer_turn)
    elif recursion != AI_DEPTH:
        return best_value_captured
    elif best_move != (-1, -1):
        print('moved normal ai move')
        logic.select_piece(board, best_move_piece[0], best_move_piece[1])
        logic.move_or_select_piece(board, best_move, logic.square_size, logic.piece_selected, computer_turn, True)
        return best_value_captured


def look_ahead_ai(board, computer_turn, recursion):
    """same as look_ahead_ai_v2"""
    enemy_color = 'b' if computer_turn else 'w'
    pieces_value = {(enemy_color + 'p') : 1, (enemy_color + 'n') : 3, (enemy_color + 'b') : 3, (enemy_color + 'r') : 5, (enemy_color + 'q') : 9, (enemy_color + 'k') : 0}
    color = 'w' if computer_turn else 'b'
    starting_val_enemy_pieces = find_pieces_value(board, not computer_turn)
    best_value_captured = -50
    best_move = (-1, -1)
    best_move_piece = (-1, -1)
    for piece in logic.find_color_pieces(board, color):
        for search_row in range(logic.dimension):
            for search_column in range(logic.dimension):
                """iterates through all the pieces and all their possible moves (iterates through 64 squares for each piece which is not efficient)"""
                potential_board = logic.verify_move_final(board, search_row, search_column, piece[0], piece[1], True, False)
                """if the move is illegal, verify_move_final will return False, otherwise it will return a new board where the move was made"""
                if potential_board:
                    enemy_pieces = logic.find_color_pieces(potential_board, enemy_color)
                    potential_min_val_enemy_pieces = 0
                    for enemy_piece in enemy_pieces:
                        enemy_piece_value = (potential_board[enemy_piece[0]])[enemy_piece[1]]
                        potential_min_val_enemy_pieces += pieces_value[enemy_piece_value]
                        """we add up all the enemy pieces' values"""

                    value_captured = starting_val_enemy_pieces - potential_min_val_enemy_pieces
                    if recursion:
                        """goes to the next depth, calling itself but with a new board where the move was made, and simulates its own or the enemy's best move, depending on who's to move"""
                        next_depth_board = logic.initialize_empty_board()
                        logic.transfer_board(next_depth_board, potential_board)
                        possible_loss_value = look_ahead_ai(next_depth_board, not computer_turn, recursion - 1)
                        value_captured -= possible_loss_value

                    if value_captured >= best_value_captured:
                        best_value_captured = value_captured
                        best_move_piece = (piece[0], piece[1])
                        best_move = (search_column, search_row)  #  "best" move by only looking one move ahead
    if recursion != AI_DEPTH:
        return best_value_captured
    elif best_move != (-1, -1):
        logic.select_piece(board, best_move_piece[0], best_move_piece[1])
        logic.move_or_select_piece(board, best_move, logic.square_size, logic.piece_selected, computer_turn, True)
        return best_value_captured


def draw_possible_moves(screen, board, row, column, color):
    """
    :param screen: the "canvas" on which everything is drawn
    :param board: the logical board
    :param row: the row of the rectangle
    :param column: the column of the rectangle
    :param color: the color of the rectangle
    """
    for search_row in range(DIMENSION):
        for search_column in range(DIMENSION):
            if logic.verify_move_final(board, search_row, search_column, row, column, False, False):
                draw_circle(screen, search_row, search_column, color)


def run(p, current_board, vs_computer, computer_turn):
    """The game itself. The board is continuously drawn, and each move only modifies the logical board,
    which is instantly drawn again
    :param p: the pygame object
    :param current_board: the board we run the game on
    :param vs_computer: whether we play agains the computer or not
    :param computer_turn: if it is the computer's turn when starting or not"""
    screen = p.display.set_mode((WIDTH, HEIGHT))
    load_images(p)
    game_finished = False
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                raw_location = p.mouse.get_pos()
                logic.move_or_select_piece(current_board, raw_to_matrix(raw_location), SQUARE_SIZE, logic.piece_selected, logic.turn, False)
        draw_board(screen)
        draw_pieces(screen, current_board)
        draw_coordinates(p, screen, (0, 0, 0))
        if logic.piece_selected:
            draw_possible_moves(screen, current_board, logic.selected_square_row, logic.selected_square_column, CIRCLE_COLOR)

        if logic.checkmated:
            game_finished = True
            write_game_finished(p, screen, logic.turn, 'checkmate')
        if logic.stalemated:
            game_finished = True
            write_game_finished(p, screen, logic.turn, 'stalemate')
        if logic.draw_by_repetition:
            game_finished = True
            write_game_finished(p, screen, logic.turn, 'draw by repetition')
        p.display.update()

        if logic.promotion_screen:
            draw_board(screen)
            draw_promotion_rectangle(screen, logic.promotion_row, logic.promotion_column, BEIGE)
            draw_pieces(screen, logic.promotion_board)
            draw_coordinates(p, screen, (0, 0, 0))
            p.display.update()
            running_promotion = True
            while running_promotion:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        running = False
                        running_promotion = False
                    if event.type == p.MOUSEBUTTONDOWN:
                        raw_location = p.mouse.get_pos()
                        location = raw_to_matrix(raw_location)
                        """if choose_promotion returns true, the promotion screen is stopped"""
                        if logic.choose_promotion(current_board, location):
                            running_promotion = False

        elif vs_computer and not game_finished:  # ai moves
            if logic.turn == computer_turn:
                look_ahead_ai_v2(current_board, computer_turn, AI_DEPTH)



def raw_to_matrix(raw_location):
    """
    :param raw_location: the actual pixel location of the click
    """
    return raw_location[0] // SQUARE_SIZE, raw_location[1] // SQUARE_SIZE


if __name__ == '__main__':
    pyg.init()
    run(pyg, BackEnd.test_board, vs_computer=True, computer_turn=False)

