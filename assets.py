import pygame

def load_image(path):
    return pygame.transform.scale(pygame.image.load(path), (60, 60))

PIECE_IMAGES = {
    'white': {
        'pawn': load_image('assets/w_pawn.png'),
        'rook': load_image('assets/w_rook.png'),
        'knight': load_image('assets/w_knight.png'),
        'bishop': load_image('assets/w_bishop.png'),
        'queen': load_image('assets/w_queen.png'),
        'king': load_image('assets/w_king.png'),
    },
    'black': {
        'pawn': load_image('assets/b_pawn.png'),
        'rook': load_image('assets/b_rook.png'),
        'knight': load_image('assets/b_knight.png'),
        'bishop': load_image('assets/b_bishop.png'),
        'queen': load_image('assets/b_queen.png'),
        'king': load_image('assets/b_king.png'),
    }
}
