import sys

from const import *

import copy
import random
import time


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.menu_music = pygame.mixer.Sound('music/menu.mp3')

        self.game_music = pygame.mixer.Sound('music/game.mp3')

        self.width = 10
        self.height = 10

        self.size = 700, 700
        self.screen = pygame.display.set_mode(self.size)

        self.play_window = pygame.Surface((500, 500))  # панель с доской
        self.play_window.fill(PLAY_WINDOW_BG)

        pygame.display.set_caption('Kings Crossing')
        pygame.display.set_icon(RED_KING)

        self.board = [[0] * self.width for _ in range(self.height // 2 - 1)]
        self.board += [[0] * (self.width // 2 - 1) + [1, 2] + [0] * (self.width // 2 - 1)]
        self.board += [[0] * (self.width // 2 - 1) + [2, 1] + [0] * (self.width // 2 - 1)]
        self.board += [[0] * self.width for _ in range(self.height // 2 + 2)]

        self.start_board = copy.deepcopy(self.board)

        self.cell_size = 50
        self.left = 0
        self.top = 0

        self.player_move = True
        self.win = False
        self.lose = False

    def run(self):
        self.main_menu()
        pygame.quit()
        sys.exit()

    def main_menu(self):
        self.menu_music.stop()
        self.menu_music.play(-5)
        self.game_music.stop()

        title_game = pygame.image.load('Images/title_sprite.png')

        menu_bg = pygame.image.load('Images/menu_bg.jpg')

        rect_title = title_game.get_rect(topleft=(self.size[0] // 7, 100))

        rect_bg = menu_bg.get_rect(topleft=(0, 0))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))

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
                    self.lose = False
                    self.win = False
                    self.play()
            if rules_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.rules()
            if exit_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

    def rules(self):
        font = pygame.font.Font(None, 30)
        text_surface1 = font.render('Играя за красного короля, захватите как можно больше клеток.', True,
                                    (0, 0, 0))
        text_surface2 = font.render(
            'Вы можете захватить несколько клеток противника,', True,
            (0, 0, 0))
        text_surface3 = font.render(
            'захватив их между двумя своего цвета.', True,
            (0, 0, 0))

        text_rect1 = text_surface1.get_rect(topleft=(self.size[0] - 670, 200))
        text_rect2 = text_surface2.get_rect(topleft=(self.size[0] - 670, 230))
        text_rect3 = text_surface3.get_rect(topleft=(self.size[0] - 670, 260))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((143, 227, 216))
            self.screen.blit(text_surface1, text_rect1)
            self.screen.blit(text_surface2, text_rect2)
            self.screen.blit(text_surface3, text_rect3)

            back_button = pygame.Rect((self.size[0] - 200) // 2, self.size[1] // 2 + 200, 200, 60)
            pygame.draw.rect(self.screen, (11, 64, 57), back_button)
            text = font.render("Назад", True, 'white')
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2, self.size[1] // 2 + 220))

            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    running = False
                    self.main_menu()

            pygame.display.flip()

    def play(self):
        self.menu_music.stop()
        self.game_music.play(-5)
        to_menu_button = pygame.Rect((self.size[0] - 200) // 2 - 200, self.size[1] // 2 - 320, 200, 60)
        font = pygame.font.Font(None, 30)
        text = font.render("В меню", True, 'black')

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(SCREEN_BG, (0, 0))
            self.screen.blit(self.play_window, (100, 100))
            pygame.draw.rect(self.screen, (247, 185, 49), to_menu_button)
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2 - 200, self.size[1] // 2 - 300))

            if self.lose or self.win:
                running = False
                self.end()

            player_cells = []
            possible_moves = []

            for x in range(self.width):
                for y in range(self.height):
                    if self.board[x][y] == 1:
                        player_cells.append((x, y))

            for cell in player_cells:
                possible_moves.append(self.get_moves(self.board[cell[0]][cell[1]]))

            if self.player_move:
                if possible_moves:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.get_click(event.pos)
                else:
                    self.lose = True
                    running = False
                    self.end()
            else:
                self.computer_move()
            mouse_pos = pygame.mouse.get_pos()
            if to_menu_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.play_window.fill(PLAY_WINDOW_BG)
                    self.board = self.start_board
                    self.main_menu()
            self.render()
            pygame.display.flip()
        pygame.quit()

    def end(self):
        font = pygame.font.Font(None, 30)
        text_surface = font.render('Текст', True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(self.size[0] - 670, 200))

        final_score = self.get_score()
        max_score = max(final_score.values())
        for k, v in final_score.items():
            if final_score[k] == max_score and k == 1:
                text_surface = font.render('Вы выиграли!', True, (0, 0, 0))
                text_rect = text_surface.get_rect(topleft=(self.size[0] - 670, 200))
            elif final_score[k] == max_score and k == 2:
                text_surface = font.render('Вы проиграли...', True, (0, 0, 0))
                text_rect = text_surface.get_rect(topleft=(self.size[0] - 670, 200))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((143, 227, 216))
            self.screen.blit(text_surface, text_rect)

            back_button = pygame.Rect((self.size[0] - 200) // 2, self.size[1] // 2 + 200, 200, 60)
            pygame.draw.rect(self.screen, (11, 64, 57), back_button)
            text = font.render("Назад", True, 'white')
            self.screen.blit(text, ((self.size[0] - text.get_width()) // 2, self.size[1] // 2 + 220))

            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.main_menu()

            pygame.display.flip()

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

    def get_click(self, mouse_pos):  # обработка нажатия, координаты
        cell = self.get_cell(mouse_pos)
        if cell and self.player_move:
            self.on_click(cell)
            print(cell)

    def get_cell(self, mouse_pos):  # активная клетка
        if (mouse_pos[0] <= self.height * self.cell_size + 100 and
                mouse_pos[1] <= self.width * self.cell_size + 100):
            return (int(mouse_pos[0] / self.cell_size - 2),
                    int(mouse_pos[1] / self.cell_size - 2))
        else:
            return None

    def on_click(self, cell_coords):  # обработка нажатия игрока, вызов хода
        if self.board[cell_coords[0]][cell_coords[1]] == 0 and self.is_moves(1, cell_coords[0], cell_coords[1]):
            self.move(1, cell_coords[0], cell_coords[1])
            self.player_move = False

    def is_moves(self, cell, x, y):  # проверка, является ли ход возможным

        temp = self.board[x][y]

        self.board[x][y] = cell

        other_tile = -1

        if cell == 1:
            other_tile = 2
        elif cell == 2:
            other_tile = 1

        tiles_to_flip = []

        for x_direction, y_direction in [[0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1], [0, 1], [1, 1], [1, 0]]:
            x_move, y_move = x, y
            x_move += x_direction
            y_move += y_direction

            if not self.on_board(x_move, y_move):
                continue

            if self.on_board(x_move, y_move) and self.board[x_move][y_move] == other_tile:

                x_move += x_direction
                y_move += y_direction

                if not self.on_board(x_move, y_move):
                    continue

                while self.board[x_move][y_move] == other_tile:
                    x_move += x_direction
                    y_move += y_direction
                    if not self.on_board(x_move, y_move):
                        break
                if not self.on_board(x_move, y_move):
                    continue
                if self.board[x_move][y_move] == cell:
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

    def on_board(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_moves(self, cell):  # возможные ходы
        valid_moves = []

        for x in range(self.width):
            for y in range(self.height):
                if self.is_moves(cell, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def move(self, cell, x, y):  # реализация хода
        tiles_to_flip = self.is_moves(cell, x, y)

        if not tiles_to_flip:
            return False

        self.board[x][y] = cell

        for x, y in tiles_to_flip:
            self.board[x][y] = cell
        return True

    def computer_move(self):  # ход ИИ

        pause = time.time() + random.randint(5, 9) * 0.1
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
            self.move(2, best_move[0], best_move[1])
            self.player_move = True
        else:
            self.win = True
            self.end()

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
