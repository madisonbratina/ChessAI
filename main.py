import pygame
import itertools
import pieces
import board

pygame.init()

(width, height) = (480, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(("CHESS AI - LET'S DO THIS!"))
background_color = (255, 255, 255)
screen.fill(background_color)

board_size = 480
block_size = int(board_size / 8)
light_squares = (232, 235, 239)
dark_squares = (125, 135, 150)

color = itertools.cycle((light_squares, dark_squares))
for x in range(0, board_size, block_size):
    for y in range(0, board_size, block_size):
        pygame.draw.rect(screen, next(color), pygame.Rect(x, y, block_size, block_size))
    next(color)


#Need to create a way of locating each square.
#Convert between A1 coordinate to [1, 1]

blackBishop = pygame.image.load('Pieces/80/BlackBishop.png')
blackBishop = pygame.transform.smoothscale(blackBishop, (60, 60))
screen.blit(blackBishop, (60, 60))

#Converts the cursors location to a set of coordinates on the board
def selected_square(num):
    for x in range(0, board_size, block_size):
        for y in range(0, board_size, block_size):
            if x <= num[0] <= x + 60 and y <= num[1] <= y + 60:
                x_coord = int(x / 60)
                y_coord = int(-(y / 60)+7)
                coord = x_coord, y_coord
    return coord



pygame.display.flip()
running = True
while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(selected_square(mouse_pos))

