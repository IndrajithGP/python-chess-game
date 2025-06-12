import pygame
from assets import PIECE_IMAGES
from constants import SQUARE_SIZE

class pieces:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.image = PIECE_IMAGES[color][self.__class__.__name__]

    def draw(self, win):
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE
        win.blit(self.image, (x, y))


class pawn(pieces):
    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1
        next_row = self.row + direction
        start_row = 6 if self.color == "white" else 1

        if 0 <= next_row < 8 and board[next_row][self.col] is None:
            moves.append((next_row, self.col))
            two_row = self.row + 2 * direction
            if self.row == start_row and board[two_row][self.col] is None:
                moves.append((two_row, self.col))

        for dc in [-1, 1]:
            c = self.col + dc
            if 0 <= c < 8 and 0 <= next_row < 8:
                target = board[next_row][c]
                if target and target.color != self.color:
                    moves.append((next_row, c))

        return moves

    def get_attack_squares(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1
        next_row = self.row + direction

        for dc in [-1, 1]:
            c = self.col + dc
            if 0 <= c < 8 and 0 <= next_row < 8:
                moves.append((next_row, c))
        return moves


class rook(pieces):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class knight(pieces):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves


class bishop(pieces):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class queen(pieces):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves


class king(pieces):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
