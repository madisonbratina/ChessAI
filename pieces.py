import pygame
import math

# white_color = (242, 242, 242)
# black_color = (0, 0, 0)

square_size = 60
highlight_square = (105, 166, 217)


def determine(move, team):
    for piece in Pieces:
        if piece.position == tuple(move) and team == piece.team:
            return True


def castling(team):
    pieces = []
    castle_locations = []
    for piece in Pieces:
        pieces.append(piece.position)

    for piece in Pieces:
        if type(piece) == Rook and piece.position == (0, 0) and team == 'White':
            if not any(elem in pieces for elem in [(1, 0), (2, 0), (3, 0)]):
                castle_locations.append([2, 0])

        if type(piece) == Rook and piece.position == (7, 0) and team == 'White':
            if not any(elem in pieces for elem in [(5, 0), (6, 0)]):
                castle_locations.append([6, 0])

        if type(piece) == Rook and piece.position == (0, 7) and team == 'Black':
            if not any(elem in pieces for elem in [(1, 7), (2, 7)]):
                castle_locations.append([1, 7])

        if type(piece) == Rook and piece.position == (7, 7) and team == 'Black':
            if not any(elem in pieces for elem in [(4, 7), (5, 7), (6, 7)]):
                castle_locations.append([5, 7])

    return castle_locations


def is_farther(start, pos1, pos2):
    # returns true if pos2 is farther away than pos1
    distance_pos1 = math.sqrt((pos1[0]-start[0])**2+(pos1[1] - start[1])**2)
    distance_pos2 = math.sqrt((pos2[0]-start[0])**2+(pos2[1] - start[1])**2)
    if distance_pos1 > distance_pos2:
        return True


class ChessPiece(pygame.sprite.Sprite):
    # Class for chess pieces

    def __init__(self, image, position, team):
        pygame.sprite.Sprite.__init__(self)
        self.piece = self
        self.team = team
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
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        capture_list = []
        x = self.position[0]
        y = self.position[1]
        x_coord = x * 60
        y_coord = (-y + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        # Possible moves listed here
        if self.team == 'White':
            move_list.append([x, y + 1])
            if self.bool <= 0:
                move_list.append([x, y + 2])
        elif self.team == 'Black':
            move_list.append([x, y - 1])
            if self.bool <= 0:
                move_list.append([x, y - 2])

        # Remove point from move_list if there are any pieces in front of this pawn
        for piece in Pieces:
            if piece.position == tuple(move_list[0]):
                move_list.remove(list(piece.position))
                break

        # Create capturable piece list and incorporate en-passant
        for piece in Pieces:
            if self.team == 'White':
                if x + 1 == piece.position[0] and y + 1 == piece.position[1]:
                    capture_list.append([x + 1, y + 1])
                if x - 1 == piece.position[0] and y + 1 == piece.position[1]:
                    capture_list.append([x - 1, y + 1])
            elif self.team == 'Black':
                if x + 1 == piece.position[0] and y - 1 == piece.position[1]:
                    capture_list.append([x + 1, y - 1])
                if x - 1 == piece.position[0] and y - 1 == piece.position[1]:
                    capture_list.append([x - 1, y - 1])
        move_list.extend(capture_list)

        for i in range(len(move_list)):
            x_coord = move_list[i][0]*60 + 30
            y_coord = (-move_list[i][1]+7)*60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)

        return move_list


class Knight(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        x_coord = self.position[0] * 60
        y_coord = (-self.position[1] + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        move_list.append([self.position[0] + 1, self.position[1] + 2])
        move_list.append([self.position[0] - 1, self.position[1] + 2])
        move_list.append([self.position[0] + 1, self.position[1] - 2])
        move_list.append([self.position[0] - 1, self.position[1] - 2])
        move_list.append([self.position[0] + 2, self.position[1] + 1])
        move_list.append([self.position[0] - 2, self.position[1] + 1])
        move_list.append([self.position[0] + 2, self.position[1] - 1])
        move_list.append([self.position[0] - 2, self.position[1] - 1])

        # Using list comprehension to rebuild the move_list with capturable pieces and team mate pieces
        move_list[:] = [move for move in move_list if not determine(move, self.team)]

        for i in range(len(move_list)):
            x_coord = move_list[i][0]*60 + 30
            y_coord = (-move_list[i][1]+7)*60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)

        return move_list


class Bishop(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        all_moves = []
        found_pieces = []
        x = self.position[0]
        y = self.position[1]
        x_coord = x * 60
        y_coord = (-y + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        for i in range(1, 8):
            all_moves.append([x + i, y + i, 45])
            all_moves.append([x - i, y + i, 135])
            all_moves.append([x + i, y - i, 225])
            all_moves.append([x - i, y - i, 315])

        for piece in Pieces:
            for item in all_moves:
                if piece.position == tuple(item[0:2]):
                    found_pieces.append(item)

        for item in all_moves:
            move_list.append(item)

        for x in all_moves:
            for a in found_pieces:
                if is_farther(list(self.position), x, a) and x[2] == a[2] and x in move_list:
                    move_list.remove(x)

        # Change list back to coordinates without angle
        for move in move_list:
            del move[2]

        # Using list comprehension to rebuild the move_list with capturable pieces and team mate pieces
        move_list[:] = [move for move in move_list if not determine(move, self.team)]

        for i in range(len(move_list)):
            x_coord = move_list[i][0]*60 + 30
            y_coord = (-move_list[i][1]+7)*60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)
        return move_list


class Rook(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        all_moves = []
        found_pieces = []
        x = self.position[0]
        y = self.position[1]
        x_coord = x * 60
        y_coord = (-y + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        for i in range(1, 8):
            all_moves.append([x + i, y, 0])
            all_moves.append([x, y + i, 90])
            all_moves.append([x - i, y, 180])
            all_moves.append([x, y - i, 270])

        for piece in Pieces:
            for item in all_moves:
                if piece.position == tuple(item[0:2]):
                    found_pieces.append(item)

        for item in all_moves:
            move_list.append(item)

        for x in all_moves:
            for a in found_pieces:
                if is_farther(list(self.position), x, a) and x[2] == a[2] and x in move_list:
                    move_list.remove(x)

        # Change list back to coordinates without angle
        for move in move_list:
            del move[2]

        # Using list comprehension to rebuild the move_list with capturable pieces and team mate pieces
        move_list[:] = [move for move in move_list if not determine(move, self.team)]

        for i in range(len(move_list)):
            x_coord = move_list[i][0]*60 + 30
            y_coord = (-move_list[i][1]+7)*60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)
        return move_list


class Queen(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        all_moves = []
        found_pieces = []
        x = self.position[0]
        y = self.position[1]
        x_coord = x * 60
        y_coord = (-y + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        for i in range(1, 8):
            all_moves.append([x + i, y, 0])
            all_moves.append([x, y + i, 90])
            all_moves.append([x - i, y, 180])
            all_moves.append([x, y - i, 270])
            all_moves.append([x + i, y + i, 45])
            all_moves.append([x - i, y + i, 135])
            all_moves.append([x + i, y - i, 225])
            all_moves.append([x - i, y - i, 315])

        for piece in Pieces:
            for item in all_moves:
                if piece.position == tuple(item[0:2]):
                    found_pieces.append(item)

        for item in all_moves:
            move_list.append(item)

        for x in all_moves:
            for a in found_pieces:
                if is_farther(list(self.position), x, a) and x[2] == a[2] and x in move_list:
                    move_list.remove(x)

        # Change list back to coordinates without angle
        for move in move_list:
            del move[2]

        # Using list comprehension to rebuild the move_list with capturable pieces and team mate pieces
        move_list[:] = [move for move in move_list if not determine(move, self.team)]

        for i in range(len(move_list)):
            x_coord = move_list[i][0] * 60 + 30
            y_coord = (-move_list[i][1] + 7) * 60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)
        return move_list


class King(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self, image, position, team)
        self.bool = 0

    def move_list(self, screen):
        move_list = []
        x = self.position[0]
        y = self.position[1]
        x_coord = x * 60
        y_coord = (-y + 7) * 60
        pygame.draw.rect(screen, highlight_square, pygame.Rect(x_coord, y_coord, 60, 60))

        move_list.append([x + 1, y, 0])
        move_list.append([x, y + 1, 90])
        move_list.append([x - 1, y, 180])
        move_list.append([x, y - 1, 270])
        move_list.append([x + 1, y + 1, 45])
        move_list.append([x - 1, y + 1, 135])
        move_list.append([x + 1, y - 1, 225])
        move_list.append([x - 1, y - 1, 315])

        # Change list back to coordinates without angle - redundant for King
        for move in move_list:
            del move[2]

        # Using list comprehension to rebuild the move_list with capturable pieces and team mate pieces
        move_list[:] = [move for move in move_list if not determine(move, self.team)]

        # Logic for Castling
        if self.bool <= 0:
            move_list.extend(castling(self.team))

        for i in range(len(move_list)):
            x_coord = move_list[i][0] * 60 + 30
            y_coord = (-move_list[i][1] + 7) * 60 + 30
            pygame.draw.circle(screen, highlight_square, (x_coord, y_coord), 10)
        return move_list


# import pieces here - determine there initial position and team
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

