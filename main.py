import pygame
import itertools
import pieces
import board

from pieces import *
from board import *

pygame.init()

(width, height) = (480, 480)
screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
pygame.display.set_caption("CHESS AI - LET'S DO THIS!")


board_size = 480
block_size = int(board_size / 8)
light_squares = (232, 235, 239)
dark_squares = (125, 135, 150)
highlight_square = (105, 166, 217)
board_colors = [light_squares, dark_squares]

MouseDown = False
MouseReleased = False
MouseMoved = False
checkmate = False
SelectedPiece = None
SelectedSquare = None
OriginalPlace = None
teams = ['Black', 'White']

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
    return None


running = True
while True:
    turn = teams[0]
    pieces = []
    under_check = None

    # ----- Check for Check and Checkmate Conditions -----
    for piece in Pieces:
        if type(piece) == King:
            if piece.under_check(screen):
                under_check = True
            if under_check:
                if piece.check_mate(screen):
                    print("CHECK MATE SON")
                else:
                    print("YOUR UNDER CHECK")

    for piece in Pieces:
        pieces.append([type(piece), piece.team])
    if not [King, 'Black'] in pieces:
        print("Black Loses")
    if not [King, 'White'] in pieces:
        print("White Loses")

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
        if event.type == pygame.MOUSEMOTION:
            MouseMoved = True

        if OriginalPlace:
            OriginalPlace.move_list(screen)

        if MouseDown and SelectedPiece:
            SelectedPiece.drag(mouse_pos)
            OriginalPlace.move_list(screen)

        if MouseDown and not SelectedPiece:
            SelectedPiece = piece_in_square(selected_square(mouse_pos), Pieces)
            # ----- Confirm White or Black Turn -----
            if SelectedPiece and SelectedPiece.team == turn:
                SelectedPiece = None
            if SelectedPiece:
                OriginalPlace = SelectedPiece
                OldPlacePosition = SelectedPiece.position
            # ----- Click and Place Pieces -----
            if OriginalPlace:
                for i in range(len(OriginalPlace.move_list(screen))):
                    if tuple(OriginalPlace.move_list(screen)[i]) == selected_square(mouse_pos):
                        OriginalPlace.update(selected_square(mouse_pos))
                        # Castling Logic - This can be made better in the future
                        if type(OriginalPlace) == King and OriginalPlace.bool == 0:
                            if selected_square(mouse_pos) == (2, 0):
                                piece_in_square((0, 0), Pieces).update([3, 0])
                            if selected_square(mouse_pos) == (6, 0):
                                piece_in_square((7, 0), Pieces).update([5, 0])
                            if selected_square(mouse_pos) == (2, 7):
                                piece_in_square((0, 7), Pieces).update([3, 7])
                            if selected_square(mouse_pos) == (6, 7):
                                piece_in_square((7, 7), Pieces).update([5, 7])

                        draw_board(screen, board_colors)
                        for piece in Pieces:
                            if piece.position == OriginalPlace.position and piece.team != OriginalPlace.team:
                                Pieces.remove(piece)
                        if type(OriginalPlace) == Pawn or type(OriginalPlace) == King:
                            OriginalPlace.bool += 1
                        teams = teams[::-1]
                        break
                if SelectedPiece is not OriginalPlace:
                    OriginalPlace = None

        if MouseReleased and SelectedPiece:
            MouseReleased = False
            # ----- Drag and Drop Pieces -----
            for i in range(len(OriginalPlace.move_list(screen))):
                if tuple(OriginalPlace.move_list(screen)[i]) == selected_square(mouse_pos):
                    SelectedPiece.update(selected_square(mouse_pos))
                    # Castling Logic - This can be made better in the future
                    if type(OriginalPlace) == King and SelectedPiece.bool == 0:
                        if selected_square(mouse_pos) == (2, 0):
                            piece_in_square((0, 0), Pieces).update([3, 0])
                        if selected_square(mouse_pos) == (6, 0):
                            piece_in_square((7, 0), Pieces).update([5, 0])
                        if selected_square(mouse_pos) == (2, 7):
                            piece_in_square((0, 7), Pieces).update([3, 7])
                        if selected_square(mouse_pos) == (6, 7):
                            piece_in_square((7, 7), Pieces).update([5, 7])
                    draw_board(screen, board_colors)
                    OriginalPlace = None
                    for piece in Pieces:
                        if piece.position == SelectedPiece.position and piece.team != SelectedPiece.team:
                            Pieces.remove(piece)
                    if type(SelectedPiece) == Pawn or type(SelectedPiece) == King:
                        SelectedPiece.bool += 1
                    teams = teams[::-1]
                    break
                else:
                    SelectedPiece.update(OriginalPlace.position)
            SelectedPiece = None
            if OriginalPlace:
                OriginalPlace.move_list(screen)

        # ----- Load pieces onto the board -----
        for piece in Pieces:
            piece.draw(screen)
        pygame.display.flip()
