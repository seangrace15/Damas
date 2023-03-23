import pygame
import sys

pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_board():
    # Dibuja el tablero
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WINDOW, color, (col * 100, row * 100, 100, 100))

def draw_pieces(board, current_turn):
    # Dibuja las piezas en el tablero
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                color = RED if piece < 0 else BLUE
                pos = (col * 100 + 50, row * 100 + 50)
                pygame.draw.circle(WINDOW, color, pos, 40)

                # Resalta las fichas con opciones de movimiento
                if piece == current_turn and any_valid_move(board, (col, row)):
                    pygame.draw.circle(WINDOW, GREEN, pos, 44, 4)

def any_valid_move(board, start):
    start_col, start_row = start
    for d_row in [-2, -1, 1, 2]:
        for d_col in [-2, -1, 1, 2]:
            end_row = start_row + d_row
            end_col = start_col + d_col

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if is_valid_move(board, start, (end_col, end_row)):
                    return True
    return False

def create_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    board[row][col] = -1  # Jugador 1
                elif row > 4:
                    board[row][col] = 1   # Jugador 2
    return board

def is_valid_move(board, start, end):
    start_col, start_row = start
    end_col, end_row = end
    start_piece = board[start_row][start_col]
    end_piece = board[end_row][end_col]

    if end_piece != 0:
        return False

    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)

    if row_diff != col_diff or row_diff not in [1, 2]:
        return False

    if row_diff == 1:
        if start_piece == -1 and end_row - start_row == 1:
            return True
        if start_piece == 1 and start_row - end_row == 1:
            return True
    elif row_diff == 2:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        middle_piece = board[middle_row][middle_col]

        if middle_piece == 0 or middle_piece == start_piece:
            return False
        if start_piece == -1 and end_row - start_row == 2:
            return True
        if start_piece == 1 and start_row - end_row == 2:
            return True

    return False

def remove_captured_piece(board, start, end):
    start_col, start_row = start
    end_col, end_row = end
    middle_col, middle_row = (start_col + end_col) // 2, (start_row + end_row) // 2
    board[middle_row][middle_col] = 0

def move_piece(board, start, end):
    if is_valid_move(board, start, end):
        board[end[1]][end[0]] = board[start[1]][start[0]]
        board[start[1]][start[0]] = 0

        # Verifica si se realizó una captura y elimina la ficha capturada
        row_diff = abs(start[1] - end[1])
        if row_diff == 2:
            remove_captured_piece(board, start, end)

def main():
    clock = pygame.time.Clock()
    board = create_board()
    selected_piece = None
    current_turn = 1  # Comienza el jugador 1 (fichas azules)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // 100, y // 100

                if not selected_piece and board[row][col] == current_turn:
                    selected_piece = (col, row)
                elif selected_piece:
                    start_piece = board[selected_piece[1]][selected_piece[0]]
                    if is_valid_move(board, selected_piece, (col, row)):
                        move_piece(board, selected_piece, (col, row))
                        current_turn = -current_turn  # Cambia el turno al otro jugador
                        selected_piece = None
                    elif board[row][col] == current_turn:
                        selected_piece = (col, row)

        draw_board()
        draw_pieces(board, current_turn)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
