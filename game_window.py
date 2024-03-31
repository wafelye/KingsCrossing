import copy
import datetime

import random
from datetime import time

import pygame

PLAY_WINDOW_BG = (255, 255, 255)
SCREEN_BG = pygame.image.load('Images/city_bg.jpg')
RED_KING = pygame.image.load('Images/red_king/sprite_0.png')
BLUE_KING = pygame.image.load('Images/blue_king/sprite_0.png')


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height // 2 - 1)]
        self.board += [[0] * (width // 2 - 1) + [1, 2] + [0] * (width // 2 - 1)]
        self.board += [[0] * (width // 2 - 1) + [2, 1] + [0] * (width // 2 - 1)]
        self.board += [[0] * width for _ in range(height // 2 + 2)]
        self.player_move = True
        self.first_move = True

    def render(self):  # отрисовка поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(play_window, (115, 38, 86), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 2)
                if self.board[x][y] == 1:
                    play_window.blit(RED_KING, (x * self.cell_size + self.left - 7, y * self.cell_size + self.top - 3))
                if self.board[x][y] == 2:
                    play_window.blit(BLUE_KING, (x * self.cell_size + self.left - 7, y * self.cell_size + self.top - 3))
                if self.board[x][y] == 3 and self.player_move:
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (
                                           x * self.cell_size + self.left + self.cell_size // 2,
                                           y * self.cell_size + self.top + self.cell_size // 2
                                       ),
                                       self.cell_size // 9)

    def set_view(self, left, top, cell_size):  # параметры поля
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def run(self):  # игровой цикл
        while True:
            if self.player_move:
                self.get_click(event.pos)
            else:
                computer_cells = []
                for x in range(self.width):
                    for y in range(self.height):
                        if self.board[x][y] == 2:
                            computer_cells.append((x, y))

                            pygame.time.delay(20)

                            if self.computer_move(computer_cells):
                                self.board[self.computer_move(computer_cells)[0]][
                                    self.computer_move(computer_cells)[1]] = 2
                                print(self.computer_move(computer_cells))
                                self.player_move = True
                            else:
                                print('Конец игры')
                                return

    def get_click(self, mouse_pos):  # обработка нажатия, координаты
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, mouse_pos):  # активная клетка
        if (mouse_pos[0] < self.height * self.cell_size and
                mouse_pos[1] < self.width * self.cell_size):
            return (int(mouse_pos[0] / self.cell_size - 2),
                    int(mouse_pos[1] / self.cell_size - 2))
        else:
            return None

    def on_click(self, cell_coords):  # обработка нажатия игрока, вызов хода
        while self.player_move and self.is_moves(1,
                                                 cell_coords[0],
                                                 cell_coords[1]):
            self.board[cell_coords[0]][cell_coords[1]] = 1
            self.player_move = False
            print(cell_coords)

    def is_moves(self, cell, x, y):  # проверка, является ли ход возможным

        self.board[x][y] = cell

        if cell == 1:
            other_tile = 2
        elif cell == 2:
            other_tile = 1

        tiles_to_flip = []

        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x_move, y_move = x, y
            x_move += x_direction
            y_move += y_direction
            if x_move < self.width and y_move < self.height and self.board[x_move][y_move] == other_tile:

                x_move += x_direction
                y_move += y_direction

                while self.board[x_move][y_move] == other_tile:
                    x_move += x_direction
                    y_move += y_direction
                if self.board[x_move][y_move] == cell:
                    # Переворачиваем фишки
                    while True:
                        x_move -= x_direction
                        y_move -= y_direction
                        if x_move == x and y_move == y:
                            break
                        tiles_to_flip.append([x_move, y_move])
                    self.board[x_move + 1][y_move + 1] = 3
        self.board[x][y] = 0
        if len(tiles_to_flip) == 0:  # Если не перевернуто ни одной фишки, ход невозможен
            return False
        return tiles_to_flip

    def get_moves(self, cell):  # возможные ходы
        valid_moves = []

        for x in range(self.width):
            for y in range(self.height):
                if self.is_moves(cell, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def is_corner(self, x, y):  # проверка, находится ли активная клетка в углу поля
        return ((x == 0 and y == 0) or
                (x == self.width and y == 0) or
                (x == 0 and y == self.height) or
                (x == self.width and y == self.height))

    def move(self, cell, x, y):  # реализация хода
        tiles_to_flip = self.is_moves(cell, x, y)

        if not tiles_to_flip:
            return False

        self.board[x][y] = cell

        for x, y in tiles_to_flip:
            self.board[x][y] = cell
        return True

    def computer_move(self, cells):  # ход ИИ

        best_move = None

        for cell in cells:
            possible_moves = self.get_moves(self.board[cell[0]][cell[1]])

            random.shuffle(possible_moves)

            for x, y in possible_moves:
                if self.is_corner(x, y):
                    return [x, y]
                else:
                    best_score = -1
                    for x1, y1 in possible_moves:  # Выбираем из всех возможных ходов самый лучший
                        self.move(self.board[cell[0]][cell[1]], x1, y1)
                        score = self.get_score()[2]
                        if score > best_score:
                            best_move = [x1, y1]
                            best_score = score
        return best_move

    def get_score(self):  # подсчет очков
        r_score = 0
        b_score = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == 1:
                    r_score += 1
                if self.board[x][y] == 2:
                    b_score += 1
        return {1: r_score, 2: b_score}


pygame.init()

board_width = 10
board_height = 10

size = board_width * 70, board_height * 70
screen = pygame.display.set_mode(size)

play_window = pygame.Surface((board_width * 50, board_height * 50))  # панель с доской
play_window.fill(PLAY_WINDOW_BG)

pygame.display.set_caption('Реверси')

board = Board(board_width, board_height)
board.set_view(0, 0, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.run()
    screen.fill((0, 0, 0))
    screen.blit(SCREEN_BG, (0, 0))
    screen.blit(play_window, (100, 100))
    board.render()
    pygame.display.flip()
pygame.quit()
