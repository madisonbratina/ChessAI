import pygame


# white_color = (242, 242, 242)
# black_color = (0, 0, 0)

square_size = 60
highlight_square = (105, 166, 217)


class ChessPiece(pygame.sprite.Sprite):
    # Class for chess pieces

    def __init__(self, image, position, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (square_size, square_size))
        self.position = position
        self.rect = pygame.Rect(self.image.get_rect())

        x_coord = self.position[0] * square_size
        y_coord = (-self.position[1] + 7) * square_size
        position = (x_coord, y_coord)
        self.rect.center = position

    def draw(self, surface):
        surface.blit(self.image, self.rect.center)

    def drag(self, cursor):
        self.rect.bottomright = cursor

    def update(self, position):
        self.position = position
        x_coord = self.position[0] * 60
        y_coord = (-self.position[1] + 7) * 60
        self.rect.center = (x_coord, y_coord)


class Pawn(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self, screen):
        move_list = []

        x_coord = self.position[0] * 60
        y_coord = (-self.position[1] + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        if self.color == 'White':
            move_list.append([self.position[0], self.position[1] + 1])
            move_list.append([self.position[0], self.position[1] + 2])
        elif self.color == 'Black':
            move_list.append([self.position[0], self.position[1] - 1])
            move_list.append([self.position[0], self.position[1] - 2])
        for i in range(len(move_list)):
            x_coord = move_list[i][0]*60 + 30
            y_coord = (-move_list[i][1]+7)*60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)

        return move_list


class Knight(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self):
        move_list = []
        print("foo")

class Bishop(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self):
        move_list = []
        print("foo")


class Rook(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self):
        move_list = []
        print("foo")


class Queen(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self):
        move_list = []
        print("foo")


class King(ChessPiece):
    def __init__(self, image, position, color):
        ChessPiece.__init__(self, image, position, color)
        self.bool = 0

    def move_list(self):
        move_list = []
        print("foo")


# import pieces here - determine there initial position and color
Pieces = [
    Pawn('Pieces/80/WhitePawn.png', (0, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (1, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (2, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (3, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (4, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (5, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (6, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (7, 1), 'White'),
    Pawn('Pieces/80/WhitePawn.png', (8, 1), 'White'),
    Pawn('Pieces/80/BlackPawn.png', (0, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (1, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (2, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (3, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (4, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (5, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (6, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (7, 6), 'Black'),
    Pawn('Pieces/80/BlackPawn.png', (8, 6), 'Black'),
    Knight('Pieces/80/WhiteKnight.png', (1, 0), 'White'),
    Knight('Pieces/80/WhiteKnight.png', (6, 0), 'White'),
    Knight('Pieces/80/BlackKnight.png', (1, 7), 'Black'),
    Knight('Pieces/80/BlackKnight.png', (6, 7), 'Black'),
    Bishop('Pieces/80/WhiteBishop.png', (2, 0), 'White'),
    Bishop('Pieces/80/WhiteBishop.png', (5, 0), 'White'),
    Bishop('Pieces/80/BlackBishop.png', (2, 7), 'Black'),
    Bishop('Pieces/80/BlackBishop.png', (5, 7), 'Black'),
    Rook('Pieces/80/WhiteRook.png', (0, 0), 'White'),
    Rook('Pieces/80/WhiteRook.png', (7, 0), 'White'),
    Rook('Pieces/80/BlackRook.png', (0, 7), 'Black'),
    Rook('Pieces/80/BlackRook.png', (7, 7), 'Black'),
    Queen('Pieces/80/WhiteQueen.png', (3, 0), 'White'),
    Queen('Pieces/80/BlackQueen.png', (4, 7), 'Black'),
    King('Pieces/80/WhiteKing.png', (4, 0), 'White'),
    King('Pieces/80/BlackKing.png', (3, 7), 'Black'),
]

