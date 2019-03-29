import itertools
import pygame


def draw_board(screen, board_colors):
    board_size = 480
    block_size = int(board_size / 8)

    color = itertools.cycle(board_colors)
    for x in range(0, board_size, block_size):
        for y in range(0, board_size, block_size):
            pygame.draw.rect(screen, next(color), pygame.Rect(x, y, block_size, block_size))
        next(color)
