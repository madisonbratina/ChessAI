import pygame
import itertools
import pieces
import board

from pieces import *
from board import *

pygame.init()

(width, height) = (480, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CHESS AI - LET'S DO THIS!")

board_size = 480
block_size = int(board_size / 8)
light_squares = (232, 235, 239)
dark_squares = (125, 135, 150)
highlight_square = (105, 166, 217)
board_colors = [light_squares, dark_squares]

MouseDown = False
MouseReleased = False
SelectedPiece = None
SelectedSquare = None
OriginalPlace = None


def selected_square(num):
    for x in range(0, board_size, block_size):
        for y in range(0, board_size, block_size):
            if x <= num[0] <= x + 60 and y <= num[1] <= y + 60:
                x_coord = int(x / 60)
                y_coord = int(-(y / 60)+7)
                coord = x_coord, y_coord
    return coord


def piece_in_square(_position, all_pieces):
    for a_piece in all_pieces:
        if _position == a_piece.position:
            return a_piece


running = True
while True:

    # Get cursor position
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        draw_board(screen, board_colors)

        if event.type == pygame.QUIT:
            running = False
        # ------ Mouse Up and Down Events ------
        if event.type == pygame.MOUSEBUTTONDOWN:
            MouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            MouseDown = False
            MouseReleased = True

        if MouseDown and SelectedPiece:
            SelectedPiece.drag(mouse_pos)
        if MouseDown and not SelectedPiece:
            SelectedPiece = piece_in_square(selected_square(mouse_pos), Pieces)
            if SelectedPiece:
                OriginalPlace = SelectedPiece
            elif not SelectedPiece:
                OriginalPlace = None
        if MouseReleased and SelectedPiece:
            MouseReleased = False
            print(selected_square(mouse_pos))
            SelectedPiece.update(selected_square(mouse_pos))
            SelectedPiece = None

        # print(SelectedPiece)
        if OriginalPlace is not None:
            # color_square(selected_square(mouse_pos))
            #print(OriginalPlace.move_list(screen))
            OriginalPlace.move_list(screen)

        # load pieces onto the board
        for piece in Pieces:
            piece.draw(screen)
        pygame.display.flip()
