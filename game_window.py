import sys

from const import *

import copy
import random
import time


class Game:
    def __init__(self):
        pygame.init()

        self.width = 10
        self.height = 10

        self.size = self.width * 70, self.height * 70
        self.screen = pygame.display.set_mode(self.size)

        self.play_window = pygame.Surface((self.width * 50, self.height * 50))  # панель с доской
        self.play_window.fill(PLAY_WINDOW_BG)

        pygame.display.set_caption('Kings Crossing')

        self.board = [[0] * self.width for _ in range(self.height // 2 - 1)]
        self.board += [[0] * (self.width // 2 - 1) + [1, 2] + [0] * (self.width // 2 - 1)]
        self.board += [[0] * (self.width // 2 - 1) + [2, 1] + [0] * (self.width // 2 - 1)]
        self.board += [[0] * self.width for _ in range(self.height // 2 + 2)]

        self.cell_size = 50
        self.left = 0
        self.top = 0

        self.player_move = True
        self.is_run = True

    def run(self):
        self.main_menu()
        pygame.quit()
        sys.exit()

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((255, 255, 255))

            # Отображение текста и кнопок меню
            title_game = pygame.image.load('Images/title_sprite.png')

            menu_bg = pygame.image.load('Images/menu_bg.jpg')

            rect_title = title_game.get_rect(topleft=(self.size[0] // 7, 100))

            rect_bg = menu_bg.get_rect(topleft=(0, 0))

            self.screen.blit(menu_bg, rect_bg)
            self.screen.blit(title_game, rect_title)

            start_button = pygame.Rect((self.size[0] - 200) // 2, self.size[1] // 2 - 30, 200, 60)
            pygame.draw.rect(self.screen, (247, 185, 49), start_button)
            font = pygame.font.Font(None, 30)
            text = font.render("Старт", True, 'black')
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2, self.size[1] // 2 - 10))

            rules_button = pygame.Rect((self.size[0] - 200) // 2, self.size[1] // 2 + 40, 200, 60)
            pygame.draw.rect(self.screen, (247, 185, 49), rules_button)
            text = font.render("Правила", True, 'black')
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2, self.size[1] // 2 + 60))

            exit_button = pygame.Rect((self.size[0] - 200) // 2, self.size[1] // 2 + 110, 200, 60)
            pygame.draw.rect(self.screen, (247, 185, 49), exit_button)
            text = font.render("Выход", True, 'black')
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2, self.size[1] // 2 + 130))

            # Обработка нажатия кнопок меню
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.play()

            elif rules_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.rules()
            elif exit_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    exit()
            pygame.display.flip()
        # while running:
        #     title = pygame.image.load('Images/title_sprite.png')
        #     image_bg = pygame.image.load('Images/city_bg.jpg')
        #
        #     image_title = image_bg.get_rect(topleft=(self.width * 70 // 2 - 300, 20))
        #
        #     self.screen.blit(title, image_title)
        #
        #     self.screen.blit(image_bg, (0, 0))
        #     self.screen.blit(image_bg,(0, 0))
        #
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #         # if event.type == pygame.USEREVENT and event.button == exit_button:
        #         #     running = False
        #         # if event.type == pygame.USEREVENT and event.button == option_button:
        #         #     self.settings_menu()
        #         # if event.type == pygame.USEREVENT and event.button == play_button:
        #         #     self.win = False
        #         #     self.game_over = False
        #
        #             self.play()

    def play(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(SCREEN_BG, (0, 0))
            self.screen.blit(self.play_window, (100, 100))
            if self.player_move:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.get_click(event.pos)
            else:
                self.computer_move()
            if not self.is_run:
                final_score = self.get_score()
                max_score = max(final_score.values())
                for k, v in final_score.items():
                    if final_score[k] == max_score and k == 1:
                        print('Вы победили!')
                    elif final_score[k] == max_score and k == 2:
                        print('Вы проиграли...')
                break
            self.render()
            pygame.display.flip()
        pygame.quit()

    def render(self):  # отрисовка поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.play_window, (115, 38, 86), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 2)
                if self.board[x][y] == 1:
                    self.play_window.blit(RED_KING,
                                          (x * self.cell_size + self.left - 7, y * self.cell_size + self.top - 3))
                if self.board[x][y] == 2:
                    self.play_window.blit(BLUE_KING,
                                          (x * self.cell_size + self.left - 7, y * self.cell_size + self.top - 3))

    def set_view(self, left, top, cell_size):  # параметры поля
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):  # обработка нажатия, координаты
        cell = self.get_cell(mouse_pos)
        if cell and self.player_move:
            self.on_click(cell)

    def get_cell(self, mouse_pos):  # активная клетка
        if (mouse_pos[0] < self.height * self.cell_size and
                mouse_pos[1] < self.width * self.cell_size):
            return (int(mouse_pos[0] / self.cell_size - 2),
                    int(mouse_pos[1] / self.cell_size - 2))
        else:
            return None

    def on_click(self, cell_coords):  # обработка нажатия игрока, вызов хода
        if self.is_moves(1, cell_coords[0], cell_coords[1]):
            self.board[cell_coords[0]][cell_coords[1]] = 1
            self.move(1, cell_coords[0], cell_coords[1])
            self.player_move = False
            print(cell_coords)
        # else:
        #     self.is_run = False

    def is_moves(self, cell, x, y):  # проверка, является ли ход возможным

        temp = self.board[x][y]

        self.board[x][y] = cell

        other_tile = -1

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
        self.board[x][y] = temp
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

    def computer_move(self):  # ход ИИ

        pause = time.time() + random.randint(5, 15) * 0.1
        while time.time() < pause:
            pygame.display.update()

        computer_cells = []

        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == 2:
                    computer_cells.append((x, y))

        best_move = None

        for cell in computer_cells:

            possible_moves = self.get_moves(self.board[cell[0]][cell[1]])
            for x, y in possible_moves:
                if self.is_corner(x, y):
                    return [x, y]
                else:
                    best_score = -1
                    for x1, y1 in possible_moves:  # Выбираем из всех возможных ходов самый лучший
                        board = copy.deepcopy(self.board)
                        self.move(2, x1, y1)
                        score = self.get_score()[2]
                        if score > best_score:
                            best_move = [x1, y1]
                            best_score = score
                        self.board = board
        if best_move:
            self.board[best_move[0]][best_move[1]] = 2

            self.move(2, best_move[0], best_move[1])
            self.player_move = True
            print(best_move[0], best_move[1])
        else:
            self.is_run = False

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


Game().run()

# running = True
# while running:
#     screen.fill((0, 0, 0))
#     screen.blit(SCREEN_BG, (0, 0))
#     screen.blit(play_window, (100, 100))
#     if board.player_move:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 board.get_click(event.pos)
#     else:
#         board.computer_move()
#     if not board.is_run:
#         final_score = board.get_score()
#         max_score = max(final_score.values())
#         for k, v in final_score.items():
#             if final_score[k] == max_score and k == 1:
#                 print('Вы победили!')
#             elif final_score[k] == max_score and k == 2:
#                 print('Вы проиграли...')
#         break
#     board.render()
#     pygame.display.flip()
# pygame.quit()
