import pygame
from constants import ROWS, COLS, SQUARE_SIZE
from pieces import pawn, rook, knight, bishop, queen, king

class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.captured_pieces = {'white': [], 'black': []}
        self.create_board()

    def create_board(self):
        order = [rook, knight, bishop, queen, king, bishop, knight, rook]
        for col, piece_class in enumerate(order):
            self.board[0][col] = piece_class('black', 0, col)
            self.board[7][col] = piece_class('white', 7, col)
        for col in range(COLS):
            self.board[1][col] = pawn('black', 1, col)
            self.board[6][col] = pawn('white', 6, col)

    def draw(self, win, selected=None, valid_moves=[]):
        colors = [(235, 235, 208), (119, 148, 85)]
        for row in range(ROWS):
            for col in range(COLS):
                color = colors[(row + col) % 2]
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                if selected and (row, col) == selected:
                    pygame.draw.rect(win, (0, 0, 255), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

                if (row, col) in valid_moves:
                    pygame.draw.rect(win, (0, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                piece = self.board[row][col]
                if piece:
                    piece.draw(win)

    def move_piece(self, start_pos, end_pos):
        sr, sc = start_pos
        er, ec = end_pos
        piece = self.board[sr][sc]
        target = self.board[er][ec]

        if target:
            self.captured_pieces[target.color].append(target)

        self.board[er][ec] = piece
        self.board[sr][sc] = None
        piece.row, piece.col = er, ec

        if isinstance(piece, pawn):
            if (piece.color == 'white' and er == 0) or (piece.color == 'black' and er == 7):
                return 'promote', (er, ec)

        return 'moved', None

    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                p = self.board[row][col]
                if p and isinstance(p, king) and p.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        for row in range(8):
            for col in range(8):
                p = self.board[row][col]
                if p and p.color != color:
                    if hasattr(p, 'get_attack_squares'):
                        attack_squares = p.get_attack_squares(self.board)
                    else:
                        attack_squares = p.get_valid_moves(self.board)

                    if king_pos in attack_squares:
                        return True

        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self.board)
                    for move in valid_moves:
                        target = self.board[move[0]][move[1]]
                        self.board[move[0]][move[1]] = piece
                        self.board[piece.row][piece.col] = None
                        old_row, old_col = piece.row, piece.col
                        piece.row, piece.col = move

                        in_check = self.is_in_check(color)

                        piece.row, piece.col = old_row, old_col
                        self.board[old_row][old_col] = piece
                        self.board[move[0]][move[1]] = target

                        if not in_check:
                            return False
        return True
    

    def filter_moves(self, piece, moves):
        safe_moves = []

        for move in moves:
            er, ec = move
            sr, sc = piece.row, piece.col
            captured = self.board[er][ec]

            # Simulate move
            self.board[er][ec] = piece
            self.board[sr][sc] = None
            old_row, old_col = piece.row, piece.col
            piece.row, piece.col = er, ec

            in_check = self.is_in_check(piece.color)

            # Undo move
            piece.row, piece.col = old_row, old_col
            self.board[sr][sc] = piece
            self.board[er][ec] = captured

            if not in_check:
                safe_moves.append(move)

        return safe_moves
